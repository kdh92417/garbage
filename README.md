# 미니 프로젝트 - 주차장정산시스템 구현

주차장 정산시스템을 구현해보는 미니프로젝트 입니다.

<br>

## 사용해본 기술

### Front : HTML, CSS

- HTML과 CSS를 이용하여 웹사이트를 꾸몃습니다.

### Back-end : Python, Django

- python과 django를 이용하여 API를 구축해보았습니다.

### Database : Mysql

- Mysql를 Django와 연동하여 클라이언트에서 온 요청을 토대로 CRUD를 구현해보았습니다.

### 배포 : AWS EC2, AWS RDS

- AWS의 ec2, rds를 생성및 연동하여 퍼블릭 IP로 배포를 해보았습니다.

<br>

## Demo Video

[![Video Label](https://user-images.githubusercontent.com/58774316/114295594-30ae9900-9ae1-11eb-9e75-9c64a7a530e5.png)](https://youtu.be/FvXWv3XBcds)

<br>

## API

- `entrance/in/` : 차량 입차 (정기차량과 손님아량 구분)
- `entrance/out/99` : 차량 출차 (정기차량과 손님아량 구분)
- `entrance/discount/99` : 요금 할인
- `entrance/payment/99` : 요금 정산
- `entrance/manager/` : 관리자(차량조회, 정기차량 등록 및 해제)
- `/` : 주차장 현황(주차장에 어떤 차량이있는지 확인)

<br>

## 주차장 설계도

<img src="https://user-images.githubusercontent.com/58774316/110206669-75cc2380-7ec2-11eb-810a-a7dd96d7f969.jpg" width="50%">

<br>

## ERD

![주차장 정산 시스템 ERD](https://user-images.githubusercontent.com/58774316/114266973-4e71f480-9a34-11eb-98f5-172fff5ba786.png)
