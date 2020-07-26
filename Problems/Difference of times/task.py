# put your python code here
first_hour = int(input())
first_min = int(input())
first_sec = int(input())

second_hour = int(input())
second_min = int(input())
second_sec = int(input())

result = second_sec - first_sec
result += second_min * 60 - first_min * 60
result += second_hour * 3600 - first_hour * 3600

print(result)
