import pandas as pd
import json


def profit(order):
    total_price = 0
    total_quantity = 0
    for product in order['products']:
        total_price += (product['price'] * product['quantity'])
        total_quantity += product['quantity']
    profit = total_price  + order['highway_cost'] * total_quantity
    return profit if profit != 0 else 1
    

def total_products(order, product_list = {}, flag = False):
    warehouse_profit = 0
    for product in order['products']:
        quantity = product['quantity']
        income = product['price'] * quantity
        expenses = order['highway_cost'] * quantity
        profit = income + expenses
        warehouse_profit += income
        if product['product'] not in product_list:
            product_list[product['product']] = {
                'product': product['product'], 
                'quantity': quantity, 
                'income': income, 
                'expenses': expenses,
                'profit': profit
            }
        else:
            product_list[product['product']]['quantity'] += quantity
            product_list[product['product']]['income'] += income
            product_list[product['product']]['expenses'] += expenses
            product_list[product['product']]['profit'] += profit
    if flag:
        product_list['warehouse_profit'] = warehouse_profit
    return product_list


def procent(row, total = [0]):
    total[0] += row['percent_profit_product_of_warehouse']
    return total[0]


def categories(row):
    if row['accumulated_percent_profit_product_of_warehouse'] <= 70:
        category = 'A'
    elif 70 < row['accumulated_percent_profit_product_of_warehouse'] <=90:
        category = 'B'
    elif row['accumulated_percent_profit_product_of_warehouse'] > 90:
        category = 'C'
    else:
        print('Error. Invalid data.')
    return category


def tasks_1(data):
    print('Тариф стоимости доставки для каждого склада')
    print('\n')
    task_1 = [(order['warehouse_name'], abs(order['highway_cost'])) for order in data]
    table = pd.DataFrame(task_1, columns=['warehouse_name', 'highway_cost'])
    print(table)
    print('\n')


def task_2(data):
    print('Суммарное количество , суммарный доход , суммарный расход и суммарная прибыль для каждого товара')
    print('\n')
    columns = ['product', 'quantity', 'income', 'expenses', 'profit']
    products_data = list()
    for order in data:
        products = total_products(order)
    for product in products.values():
            products_data.append([product['product'], product['quantity'], product['income'], product['expenses'], product['profit']]) 
    table = pd.DataFrame(products_data, columns=columns)
    print(table)
    print('\n\n')


def task_3(data):
    print('Прибыль с заказа. Средняя прибыль.')
    print('\n')
    columns = ['order_id', 'order_profit']
    table_data = {order['order_id']: profit(order) for order in data}
    table = pd.DataFrame(table_data.items(), columns=columns)
    average_profit = sum(table_data.values()) / len(table_data)
    print(table)
    print(f'Average profit: {average_profit}')
    print('\n\n')


def task_4(data):
    print('Процент прибыли продукта заказанного из определенного склада к прибыли этого склада')
    print('\n')
    columns = ['warehouse_name', 'product', 'quantity', 'profit', 'percent_profit_product_of_warehouse']
    table_data = list()
    for order in data:
        products = total_products(order, product_list = {}, flag = True)
        warehouse_profit = products.pop('warehouse_profit')
        for product in products.values():
            percent_profit = round(100 / warehouse_profit * product['income'], 2)
            product_data = [order['warehouse_name'], product['product'], product['quantity'], product['profit'], percent_profit]
            table_data.append(product_data)
        break
    table = pd.DataFrame(table_data, columns=columns)
    print(table)
    print('\n\n')
    return table


def task_5(table):
    print('Сортировка по убыванию процента, подсчет накопленного процента.')
    print('\n')
    table = table.sort_values(by='percent_profit_product_of_warehouse', ascending=False)
    table['accumulated_percent_profit_product_of_warehouse'] = table.apply(lambda row: procent(row), axis=1)
    print(table)
    print('\n\n')
    return table


def task_6(table):
    print('Категории на основании значения накопленного процента.')
    print('\n')
    table['category'] = table.apply(lambda row: categories(row), axis=1)
    print(table)


def main():
    with open('data.json', 'r', encoding='utf-8') as data:
        data = json.load(data)
        tasks_1(data)
        task_2(data)
        task_3(data)
        table = task_4(data)
        table = task_5(table)
        task_6(table)
        


if __name__ == '__main__':
    main()