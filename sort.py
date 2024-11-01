arr = [2, 5, 1, 9, 7, 15, 0]

def get_max_min(arr):
    max_num = arr[0]
    min_num = arr[0]
    for num in arr:
        if num > max_num:
            max_num = num
        if num < min_num:
            min_num = num
    return max_num, min_num


                     

def my_sort(arr):
    max_num, min_num = get_max_min(arr)
    sorted_arr = [0] * (max_num - min_num + 1)
    for num in arr:
        sorted_arr[num - min_num] = num
    return sorted_arr

