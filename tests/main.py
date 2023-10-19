from lazython import Lazython


if __name__ == '__main__':

    lazyier = Lazython()

    tab1 = lazyier.new_tab(name='Tab 1', subtabs=['Subtab 1', 'Subtab 2', 'Subtab 3'])

    line1_1 = tab1.add_line(text='Line 1', subtexts=['Subtext 1', 'Subtext 2', 'Subtext 3'])
    line1_2 = tab1.add_line(text='Line 2', subtexts=['Subtext 1', 'Subtext 2', 'Subtext 3'])
    line1_3 = tab1.add_line(text='Line 3', subtexts=['Subtext 1', 'Subtext 2', 'Subtext 3'])
    line1_4 = tab1.add_line(text='Line 4', subtexts=[''.join([f'Subtext 1.{i}\n' for i in range(100)])])
    line1_5 = tab1.add_line(text='Line 5')
    line1_6 = tab1.add_line(text='Line 6')

    tab2 = lazyier.new_tab(name='Tab 2', height_weight=0.4)

    line2_1 = tab2.add_line(text='Line 1')
    line2_2 = tab2.add_line(text='Line 2')
    line2_3 = tab2.add_line(text='Line 3')
    line2_4 = tab2.add_line(text='Line 4')
    line2_5 = tab2.add_line(text='Line 5')
    line2_6 = tab2.add_line(text='Line 6')
    line2_7 = tab2.add_line(text='Line 7')
    line2_8 = tab2.add_line(text='Line 8')
    line2_9 = tab2.add_line(text='Line 9')

    tab3 = lazyier.new_tab(name='Tab 3')

    line3_1 = tab3.add_line(text='Line 1')
    line3_2 = tab3.add_line(text='Line 2')
    line3_3 = tab3.add_line(text='Line 3')
    line3_4 = tab3.add_line(text='Line 4')
    line3_5 = tab3.add_line(text='Line 5')

    lazyier.start()
