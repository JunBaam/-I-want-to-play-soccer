import random
from django.core.management.base import BaseCommand
from django_seed import Seed
# 2중 리스트를 일차원 리스트로 만들어줌.
from django.contrib.admin.utils import flatten
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "price": lambda x: random.randint(20000, 30000),
                "room_type": lambda x: random.choice(room_types),
                # "location": lambda x: seeder.faker.address(),

            },
        )
        # 방에 사진을 넣는 부분
        created_photos = seeder.execute()
        # Django flatten : 이중리스트를 단일 리스트로 바꿔준다.
        created_clean = flatten(list(created_photos.values()))
        # 편의 시설 모델
        facilities = room_models.Facility.objects.all()
        for pk in created_clean:
            # primary key로 방으 찾음
            room = room_models.Room.objects.get(pk=pk)
            # 최소 3개 , 5~13장 생성
            for i in range(3, random.randint(5, 7)):
                room_models.Photo.objects.create(
                    title=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 13)}.jpg",
                )

            for f in facilities:
                magic_number = random.randint(2, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))