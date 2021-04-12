import re
from django.http        import HttpResponseRedirect
from django.urls        import reverse

from django.shortcuts   import (
    render,
)

from datetime           import (
    datetime,
    timedelta
)

from django.views       import View

from .models            import (
    Car,
    Record,
    PaymentRecord
)


class InView(View):
    def get(self, request):
        return render(request, 'entrance/in.html')

    def post(self, request):
        res = {}
        number = request.POST.get('number', None)

        # 차량넘버가 입력되지않으면 예외처리
        if number == None or number == '':

            res['error'] = '차량번호를 입력해주세요'
            return render(request, 'entrance/open.html', res)

        try:
            if re.match("[0-9]{2}[가-힣]{1}[0-9]{4}", number) == None:
                res['error'] = '잘못된 차량번호입니다. ex) 17도2818 '
                return render(request, 'entrance/open.html', res)
            elif re.match("[0-9]{2}[가-힣]{1}[0-9]{4}", number).group() != number:
                res['error'] = '잘못된 차량번호입니다. ex) 17도2818 '
                return render(request, 'entrance/open.html', res)
            car = Car.objects.get(number=number)

        # 정기차량으로 등록되지 않으면 Guest로 차량 등록
        except Car.DoesNotExist:
            car = Car(
                number = number,
                type = 'Guest',
            )
            car.save()

        # 중복으로 들어오는 차량 예외처리
        car_filter = {
            'car_id': car.id,
            'entry_time__isnull': False,
            'departure_time__isnull' : True
        }
        if Record.objects.filter(**car_filter):
            res['error'] = '{} 차량이 이미 주차장에 있습니다.'.format(car.number)
            return render(request, 'entrance/open.html', res)

        # 정상적으로 입차했을 경우
        time = datetime.now()
        record = Record(
            entry_time=time,
            car_id=car.id,
        )
        record.save()
        res['door'] = '{} 차량이 주차장에 들어왔습니다.'.format(car.number)
        res['car'] = car
        return render(request, 'entrance/open.html', res)


class OutView(View):
    def get(self, request, car_id):
        res = {}
        try:
            car = Car.objects.get(id=car_id)
            res = {
                'car' : car
            }
            return render(request, 'entrance/out.html', res)

        except Car.DoesNotExist:
            res['error'] = '잘못된 차량번호 입니다.'
            return render(request, 'entrance/search_car.html', res)

    def post(self, request, car_id):
        res = {}
        # selected_related 또는 prefetch_related 로 쿼리 덜 수행하게 만들 수 있을 것 같다. 리팩토링 할 떄 해보기

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            if car_id == 0:
                car_num = request.POST.get('car_num')
                try:
                    car = Car.objects.get(number=car_num)
                    return HttpResponseRedirect(reverse('entrance:out', args=(car.id,)))
                except Car.DoesNotExist:
                    res['error'] = '잘못된 차량번호 입니다.'
                    return render(request, 'entrance/open.html', res)
            res['error'] = '잘못된 차량번호 입니다.'
            return render(request, 'entrance/open.html', res)

        car_filter = {
            'car_id': car.id,
            'entry_time__isnull' : False,
            'departure_time__isnull': True
        }
        try:
            record = Record.objects.filter(**car_filter)[0]
            departure_time = datetime.now()
            entry_time = record.entry_time
            parking_time = (departure_time - entry_time).seconds / 10
            record.departure_time = departure_time
            record.parking_time = parking_time
            record.save()

            if car.type == 'Member':
                res['member'] = '정기회원 이십니다. 차단기를 오픈합니다. '
                return render(request, 'entrance/open.html', res)
            # Guest 일경우
            else:
                fare = (parking_time // 1) * 1000
                payment = PaymentRecord(
                    record_id = record.id,
                    paid_amount = fare,
                )
                payment.save()
                return HttpResponseRedirect(reverse('entrance:discount', args=(record.id,)))

        # 중복차량일 경우 예외처리
        except IndexError:
            res['error'] = '잘못된 차량번호입니다. index_error'
            return render(request, 'entrance/open.html', res)


class DiscountView(View):
    def get(self, request, record_id):
        record = Record.objects.get(id=record_id)
        res = {
            'record' : record
        }
        return render(request, 'entrance/discount.html', res)

    def post(self, request, record_id):
        coupon = request.POST.get('coupon', None)

        if coupon != None and coupon != '':
            payment = PaymentRecord.objects.get(record_id=record_id)

            try:
                discount_table = {
                    'A': 5000,
                    'B': 10000,
                    'C': 15000,
                    'D': 30000,
                    'E': 100000
                }
                discount = discount_table[coupon]
                payment.discount_amount = discount
                payment.save()

            except KeyError:
                return HttpResponseRedirect(reverse('entrance:discount', args=(record_id,)))

            total_fare = max(0, payment.paid_amount - payment.discount_amount)
            payment.total_paid_amount = total_fare
            payment.save()

        return HttpResponseRedirect(reverse('entrance:payment', args=(record_id,)))


class PaymentView(View):

    def get(self, request, record_id):
        record = Record.objects.get(id=record_id)
        car = Car.objects.get(id=record.car_id)
        payment = PaymentRecord.objects.get(record_id=record_id)

        res_data = {
            'record': payment,
            'car': car
        }

        return render(request, 'entrance/payment.html', res_data)

    def post(self, request, record_id):
        res = {
            'exit' : '정상적으로 정산 완료되셨습니다. 도어가 열립니다.'
        }
        payment_method = request.POST.get('payment_method', None)
        payment = PaymentRecord.objects.get(record_id=record_id)
        payment.paid_time = datetime.now()
        payment.payment_success = True
        payment.payment_method = payment_method
        payment.save()

        return render(request, 'entrance/open.html', res)


class ManagerView(View):
    def get(self, request):
        return render(request, 'entrance/manager.html')


class CarManagerView(View):
    def get(self, request):
        res = {}
        car_num = request.GET.get('car_num', None)
        try:
            car = Car.objects.get(number=car_num)
            res['search_car'] = car

        except Car.DoesNotExist:
            res['error'] = '존재 하지 않는 차량번호 입니다.'

        return render(request, 'entrance/manager.html', res)

    def post(self, request):
        res = {}
        car_num = request.POST.get('car_num', None)
        try:
            car = Car.objects.get(number=car_num)
            if car.type == 'Guest':
                year = datetime.today().year
                month = datetime.today().month
                day = datetime.today().day
                start_date = datetime(year , month , day)
                expire_date = start_date + timedelta(days=30)
                car.type = 'Member'
                car.start_date = start_date
                car.expire_date = expire_date
                car.save()
                res['search_car'] = car
                res['register'] = '{} 차량등록이 완료되었습니다.'.format(car.number)

            elif car.type == 'Member':
                res['register'] = '{} 차량등록이 해지되었습니다.'.format(car.number)
                car.type = 'Guest'
                car.start_date = None
                car.expire_date = None
                car.save()

        except Car.DoesNotExist:
            res['error'] = '존재 하지 않는 차량번호 입니다.'

        return render(request, 'entrance/manager.html', res)