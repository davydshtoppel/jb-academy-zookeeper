# put your python code here
duration_days = int(input())
food_cost_per_day = int(input())
one_way_fly_cost = int(input())
hotel_day_cost = int(input())

result = one_way_fly_cost * 2
result += food_cost_per_day * duration_days
result += hotel_day_cost * (duration_days - 1)

print(result)
