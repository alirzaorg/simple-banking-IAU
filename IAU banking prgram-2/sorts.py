from typing import List


class Sorting:

    def __init__(self, arr, field: str, method: str = ""):
        self.arr = arr
        self.field = field
        self.len = len(arr)

        if self.len < 20 or method == "مرتب سازی درجی":
            self.insertion_sort()
            return

        if method == "حبابی":
            self.bubble_sort()
            return

        if self.len > 10 ** 7 or method == "شمارشگر":
            self.counting_sort()
            return

        self.heap_sort()

    def selection_sort(self) -> None:
        """
        لیست lst را به صورت مرتب درجا تغییر می‌دهد، بدین صورت که کوچکترین عنصر را انتخاب کرده و با عنصری که در اندیس
        متناظر قرار دارد جابه‌جا می‌کند.

       پیچیدگی زمانی: O(n^2)
           پیچیدگی فضایی  : O(1)
       ساده و غیرپایدار
        """
        for i in range(self.len):
            min_index = i
            for j in range(i + 1, self.len):
                # Update minimum index
                if self.arr[j][self.field] < self.arr[min_index][self.field]:
                    min_index = j

            # تعویض اندیس فعلی با کوچکترین عنصر در باقیمانده لیست
            self.arr[min_index], self.arr[i] = self.arr[i], self.arr[min_index]

    def bubble_sort(self) -> None:
        """
        لیست را به گونه ای تغییر می دهد که با جابه‌جایی عناصر مجاور مرتب شود تا زمانی که کل لیست مرتب شود.

           پیچیدگی زمانی: O(n^2)؛ پیچیدگی فضایی: O(1)

          ساده و پایدار
        """
        has_swapped = True
        # اگر هیچ جابه‌جایی رخ نداده باشد، لیست مرتب است
        while has_swapped:
            has_swapped = False
            for i in range(self.len - 1):
                if self.arr[i][self.field] > self.arr[i + 1][self.field]:
                    # Swap adjacent elements
                    self.arr[i], self.arr[i + 1] = self.arr[i + 1], self.arr[i]
                    has_swapped = True

    def insertion_sort(self) -> None:

        for i in range(1, self.len):
            current_index = i

            while current_index > 0 and self.arr[current_index][self.field] < self.arr[current_index - 1][self.field]:
                # Swap elements that are out of order
                self.arr[current_index], self.arr[current_index - 1] = \
                    self.arr[current_index - 1], self.arr[current_index]
                current_index -= 1

    def heap_sort(self) -> None:

        # پیچیدگی زمانی: O(logN)
        def max_heapify(heap_size, index):
            left, right = 2 * index + 1, 2 * index + 2
            largest = index
            if left < heap_size and self.arr[left][self.field] > self.arr[largest][self.field]:
                largest = left
            if right < heap_size and self.arr[right][self.field] > self.arr[largest][self.field]:
                largest = right
            if largest != index:
                self.arr[index][self.field], self.arr[largest][self.field] = \
                    self.arr[largest][self.field], self.arr[index][self.field]
                max_heapify(heap_size, largest)

        # تبدیل لیست اصلی به heapify
        for i in range(self.len // 2 - 1, -1, -1):
            max_heapify(self.len, i)

        # پیچیدگی زمانی: O(N)
        # استفاده از هیپ برای برای مرتب سازی عناصر
        for i in range(self.len - 1, 0, -1):
            # جابجایی عنصر اخر با اول
            self.arr[i], self.arr[0] = self.arr[0], self.arr[i]
            # اندازه هیپ را در هر تکرار یک واحد کاهش می‌دهیم.
            max_heapify(i, 0)

    def counting_sort(self) -> None:

        k = max(self.arr)
        counts = [0 for _ in range(k + 1)]
        for element in self.arr:
            counts[element] += 1

        starting_index = 0
        for i, count in enumerate(counts):
            counts[i] = starting_index
            starting_index += count

        sorted_lst = [0 for _ in range(self.len)]

        for element in self.arr:
            sorted_lst[counts[element]] = element

            counts[element] += 1

        for i in range(self.len):
            self.arr[i] = sorted_lst[i]


def binary_search(arr: List[dict], field: str, query: str) -> int:
    """


    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid][field] > query:
            high = mid - 1
        elif arr[mid][field] < query:
            low = mid + 1
        else:
            return mid

    return -1
"""
