import json

from django.shortcuts   import (
    render,
    redirect
)

from django.views       import View
from datetime           import (
    datetime,
    timedelta
)

from django.views.generic   import TemplateView

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
            car = Car.objects.get(number=number)
            # 중복으로 들어올 수 있는 차량 예외처리 해야됨

        # 정기차량으로 등록되지 않으면 Guest로 차량 등록
        except Car.DoesNotExist:
            car = Car(
                number = number,
                type = 'Guest',
            )
            car.save()

        res['door'] = '{} 차량이 주차장에 들어왔습니다.'.format(car.number)
        time = datetime.now()
        record = Record(
            entry_time=time,
            car_id=car.id,
        )
        record.save()

        return render(request, 'entrance/open.html', res)


class OutView(View):
    def get(self, request):
        return render(request, 'entrance/out.html')

    def post(self, request):
        res = {}
        number = request.POST.get('number', None)
        # selected_related 또는 prefetch_related 로 쿼리 덜 수행하게 만들 수 있을 것 같다. 리팩토링 할 떄 해보기

        try:
            car = Car.objects.get(number=number)
        except Car.DoesNotExist:
            res['error'] = '잘못된 차량번호 입니다.'
            return render(request, 'entrance/open.html', res)

        car_filter = {
            'car_id': car.id,
            'entry_time__isnull' : False,
            'departure_time__isnull': True
        }

        try:
            record = Record.objects.filter(**car_filter)[0]
            print(1)
            departure_time = datetime.now()
            entry_time = record.entry_time
            parking_time = (departure_time - entry_time).seconds / 60
            print(2)
            record.departure_time = departure_time
            record.parking_time = parking_time
            record.save()
            if car.type == 'Member':
                res['door'] = '정기회원 이십니다. 차단기를 오픈합니다. '
                return render(request, 'entrance/open.html', res)
            # Guest 일경우
            else:
                fare = (parking_time // 30) * 1000
                payment = PaymentRecord(
                    record_id = record.id,
                    paid_amount = fare
                )
                payment.save()
                payment = PaymentRecord.objects.get(record_id=record.id)
                res_data = {
                    'record' : payment,
                    'car' : car
                }
                return render(request, 'entrance/payment.html', res_data)

        # 중복차량일 경우 예외처리
        except IndexError:
            res['error'] = '잘못된 차량번호입니다. index_error'
            return render(request, 'entrance/open.html', res)


class PaymentView(TemplateView):
    template_name = 'entrance/payment.html'

    def post(self, request):
        coupon = request.POST.get('coupon', None)
        discount_table = {
            'A' : 5000,
            'B' : 10000,
            'C' : 15000,
            'D' : 30000,
            'F' : 100000
        }

        discount_amount = discount_table[coupon]
        total_paid_amount = abs()

# class PayView(TemplateView):
#
#     def post(self, request):
#         car_num = request.POST.get('car_num', None)
#         car = Car.objects.get(number=car_num)
#         record =
#         car_filter = {
#             'car_id': car.id,
#             'entry_time__isnull': False,
#             'departure_time__isnull': True
#         }




