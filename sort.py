import random
import sys

import matplotlib.pyplot as plot
import matplotlib.animation as anim
import time

time_to_sort = 0


def main():

    # Function to swap two objects' (i, j) places in an array (A)
    def swap(arr, i, j):
        a = arr[j]
        arr[j] = arr[i]
        arr[i] = a

    def bubble_sort(arr):
        global time_to_sort
        tic = time.perf_counter()
        if len(arr) == 1:
            return
        for i in range(len(arr) - 1):
            for j in range(len(arr) - 1 - i):
                toc = time.perf_counter()
                time_to_sort = toc - tic
                if arr[j] > arr[j + 1]:
                    swap(arr, j, j + 1)
                yield arr

    def insertion_sort(arr):
        global time_to_sort
        tic = time.perf_counter()
        if len(arr) == 1:
            return
        for i in range(1, len(arr)):
            j = i
            while j > 0 and arr[j - 1] > arr[j]:
                toc = time.perf_counter()
                time_to_sort = toc - tic
                swap(arr, j, j - 1)
                j -= 1
                yield arr

        toc = time.perf_counter()
        time_to_sort = toc - tic

    """
    def quick_sort(arr, p, q, tic, reset_timer=False):
        if reset_timer:
            global time_to_sort
            tic = time.perf_counter()
    
        if p >= q:
            return
        piv = arr[q]
        piv_ind = p
        for i in range(p, q):
            toc = time.perf_counter()
            time_to_sort = toc - tic
            if arr[i] < piv:
                swap(arr, i, piv_ind)
                piv_ind += 1
            yield arr
        swap(arr, q, piv_ind)
        yield arr
    
        yield from quick_sort(arr, p, piv_ind - 1, tic)
        yield from quick_sort(arr, piv_ind + 1, q, tic)"""

    def quick_sort(a, l, r, tic, reset_timer=False):
        if reset_timer:
            global time_to_sort
            tic = time.perf_counter()
        if l >= r:
            return
        x = a[l]
        j = l
        for i in range(l + 1, r + 1):
            toc = time.perf_counter()
            time_to_sort = toc - tic
            if a[i] <= x:
                j += 1
                a[j], a[i] = a[i], a[j]
            yield a
        a[l], a[j] = a[j], a[l]
        yield a

        yield from quick_sort(a, l, j - 1, tic)
        yield from quick_sort(a, j + 1, r, tic)

    def selection_sort(arr):
        global time_to_sort
        tic = time.perf_counter()

        for i in range(len(arr) - 1):
            minimum = i
            for j in range(i + 1, len(arr)):
                toc = time.perf_counter()
                time_to_sort = toc - tic
                if arr[j] < arr[minimum]:
                    minimum = j
                yield arr
            if minimum != i:
                swap(arr, i, minimum)
                yield arr

    def merge_sort(arr, left, right, tic, reset_timer=False):
        if reset_timer:
            global time_to_sort
            tic = time.perf_counter()

        if right <= left:
            toc = time.perf_counter()
            time_to_sort = toc - tic
            return
        elif left < right:
            toc = time.perf_counter()
            time_to_sort = toc - tic
            mid = (left + right) // 2
            yield from merge_sort(arr, left, mid, tic)
            yield from merge_sort(arr, mid + 1, right, tic)
            yield from merge(arr, left, mid, right, tic)
            yield arr

        toc = time.perf_counter()
        time_to_sort = toc - tic

    def merge(arr, lb, mid, ub, tic):
        global time_to_sort
        new = []
        i = lb
        j = mid + 1
        while i <= mid and j <= ub:
            toc = time.perf_counter()
            time_to_sort = toc - tic
            if arr[i] < arr[j]:
                new.append(arr[i])
                i += 1
            else:
                new.append(arr[j])
                j += 1
        if i > mid:
            while j <= ub:
                toc = time.perf_counter()
                time_to_sort = toc - tic
                new.append(arr[j])
                j += 1
        else:
            while i <= mid:
                toc = time.perf_counter()
                time_to_sort = toc - tic
                new.append(arr[i])
                i += 1
        for i, val in enumerate(new):
            toc = time.perf_counter()
            time_to_sort = toc - tic
            arr[lb + i] = val
            yield arr

    def shell_sort(arr, tic, reset_timer=False):

        if reset_timer:
            global time_to_sort
            tic = time.perf_counter()

        sublistcount = len(arr) // 2
        while sublistcount > 0:
            for start_position in range(sublistcount):
                yield from gap_insertion_sort(arr, start_position, sublistcount, tic)
            sublistcount = sublistcount // 2

        toc = time.perf_counter()
        time_to_sort = toc - tic

    def gap_insertion_sort(nlist, start, gap, tic):
        global time_to_sort
        for i in range(start + gap, len(nlist), gap):

            current_value = nlist[i]
            position = i

            while position >= gap and nlist[position - gap] > current_value:
                toc = time.perf_counter()
                time_to_sort = toc - tic
                nlist[position] = nlist[position - gap]
                position = position - gap
                yield nlist

            nlist[position] = current_value
            yield nlist

    def heapify(arr, n, i):
        largest = i
        l = i * 2 + 1
        r = i * 2 + 2
        while l < n and arr[l] > arr[largest]:
            largest = l
        while r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            swap(arr, i, largest)
            yield arr
            yield from heapify(arr, n, largest)

    def heap_sort(arr):
        global time_to_sort
        tic = time.perf_counter()

        n = len(arr)
        for i in range(n, -1, -1):
            toc = time.perf_counter()
            time_to_sort = toc - tic
            yield from heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            toc = time.perf_counter()
            time_to_sort = toc - tic
            swap(arr, 0, i)
            yield arr
            yield from heapify(arr, i, 0)

    def count_sort(arr):
        global time_to_sort
        tic = time.perf_counter()

        max_val = max(arr)
        m = max_val + 1
        count = [0] * m

        for a in arr:
            toc = time.perf_counter()
            time_to_sort = toc - tic
            count[a] += 1
            yield arr
        i = 0
        for a in range(m):
            toc = time.perf_counter()
            time_to_sort = toc - tic
            for c in range(count[a]):
                arr[i] = a
                i += 1
                yield arr
            yield arr

        toc = time.perf_counter()
        time_to_sort = toc - tic

    def choose_nums():
        while True:
            try:
                num_count = int(input("\nValitse järjestettävien elementtien lukumäärä: "))
                if num_count >= 2:
                    break
                else:
                    print('Elementtien lukumäärä ei voi olla pienempi kuin 2')
            except ValueError:
                print('\nVirheellinen syöte. Kirjoita elementtien määrä kokonaislukuna.')

        return num_count

    def choose_array(num_count):
        while True:
            print('\nHaluatko järjestää luvut \n1. 1 - elementtien lukumäärä\n2. satunnaisia lukuja')
            random_choice = int(input('Valitse 1 tai 2: '))
            if random_choice == 1 or random_choice == 2:
                break
            else:
                print('\nVirheellinen syöte')

        if random_choice == 1:
            # 1 - num_count satunnaisessa järjestyksessä
            array = [i + 1 for i in range(num_count)]
            random.shuffle(array)
        elif random_choice == 2:
            # num_count lukumäärä satunnaisia lukuja välillä 1 - num_count
            array = []
            for i in range(num_count):
                random_number = random.randint(1, num_count)
                array.append(random_number)

        old_array = array.copy()
        return array, old_array

    def choose_algo(num_count, array):
        while True:
            print("\nValitse järjestysalgoritmi: \n 1. Bubble \n 2. Insertion \n 3. Quick \n 4. Selection \n 5. Merge "
                  "Sort \n 6. Shell sort \n 7. Heap sort \n 8. Count sort \n 9. Vaihda numerot ")
            sort_choice = int(input('Valitse: '))

            if sort_choice == 1:
                title = "Bubble Sort"
                algo = bubble_sort(array)
            elif sort_choice == 2:
                title = "Insertion Sort"
                algo = insertion_sort(array)
            elif sort_choice == 3:
                title = "Quick Sort"
                algo = quick_sort(array, 0, num_count - 1, 0, True)
            elif sort_choice == 4:
                title = "Selection Sort"
                algo = selection_sort(array)
            elif sort_choice == 5:
                title = "Merge Sort"
                algo = merge_sort(array, 0, num_count - 1, 0, True)
            elif sort_choice == 6:
                title = "Shell Sort"
                algo = shell_sort(array, 0, True)
            elif sort_choice == 7:
                title = "Heap Sort"
                algo = heap_sort(array)
            elif sort_choice == 8:
                title = "Count Sort"
                algo = count_sort(array)
            elif sort_choice == 9:
                return None, None
            else:
                print('\nVirheellinen syöte. Valitse 1 - 10.')

            if sort_choice in range(1, 11):
                return title, algo

    num_count = choose_nums()
    array, old_array = choose_array(num_count)

    def draw_plot(num_count, array, title, algo):
        colors = []
        for num in array:
            red_value = num / num_count
            blue_value = 1 - red_value
            color_tuple = (red_value, 0, blue_value)
            colors.append(color_tuple)

        plot.clf()
        plot.close()
        fig, ax = plot.subplots()
        ax.set_title(title)

        bar_rec = ax.bar(range(len(array)), array, align='edge', color=colors)

        ax.set_xlim(0, num_count)
        ax.set_ylim(0, int(num_count * 1.1))

        text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

        epochs = [0]

        def update_plot(array, rec, epochs):
            colors = []

            for rect in bar_rec.get_children():
                num = rect.get_height()
                red_value = (num / num_count)
                blue_value = 1 - red_value
                color_tuple = (red_value, 0, blue_value)
                colors.append(color_tuple)
                rect.set_facecolor(color_tuple)
            for rec, val in zip(rec, array):
                rec.set_height(val)
            epochs[0] += 1
            text.set_text("Vertailujen lukumäärä: {}, Aikaa kulunut: {:.4f} sekuntia".format(epochs[0], time_to_sort))

        anima = anim.FuncAnimation(fig, func=update_plot, fargs=(bar_rec, epochs), frames=algo, interval=1,
                                   repeat=False)

        plot.show()

        print(f"Aika: {time_to_sort:0.4f} sekuntia, operaatioiden lkm: {epochs[0]} ")

    while True:
        title, algo = choose_algo(num_count, array)
        if title is None:
            num_count = choose_nums()
            array, old_array = choose_array(num_count)
            title, algo = choose_algo(num_count, array)
        draw_plot(num_count, array, title, algo)
        array = old_array.copy()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n\t\tOhjelma keskeytetty \n\t\tMoikka!\n')
        sys.exit(0)
