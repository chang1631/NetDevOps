# import level1
#
# level1.l1_printer(2,3)
#
# # from level1.level1_module import l1_module_printer
# # l1_module_printer('test_l1')
#
# from level1.level2 import l2_a, l2_printer
# from level1.level2.level2_module import l2_module_printer, l2_c
#
# l2_printer(l2_c)
# l2_module_printer(l2_a)

import module3_reload
print(module3_reload.X,module3_reload.Y)

import module3_reload
print(module3_reload.X,module3_reload.Y)

import module4
module4.greeting('Welcome to use this module')
print(module4.__name__)