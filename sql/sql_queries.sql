
# table categories
CREATE EXTENSION IF NOT EXISTS ltree;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    path LTREE NOT NULL,
    CONSTRAINT path_unique UNIQUE(path)
);


2.1
SELECT c.name AS customer_name, SUM(oi.quantity * oi.price) AS total_sum
FROM customers c JOIN orders o ON c.id = o.customer_id
                JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.name
ORDER BY total_sum;


2.2
SELECT parent.id AS category_id, parent.name AS category_name, COUNT(child.id) AS child_count
FROM categories parent 
    LEFT JOIN categories child 
    ON child.path <@ parent.path AND nlevel(child.path) = nlevel(parent.path) + 1
GROUP BY parent.id, parent.name
ORDER BY parent.id;


2.3.1
CREATE OR REPLACE VIEW top_5_products_last_month AS
SELECT p.name AS product_name, 
       root.name AS top_category_name,
       SUM(oi.quantity) AS total_quantity
FROM order_items oi JOIN orders o ON oi.order_id = o.id
                    JOIN products p ON oi.product_id = p.id
                    JOIN categories c ON p.category_id = c.id
                    JOIN categories root ON root.id = (
                        SELECT id FROM categories WHERE path = subpath(c.path, 0, 1)::text
                        )
WHERE o.created_at >= (CURRENT_DATE - INTERVAL '1 month')
GROUP BY p.name, root.name
ORDER BY total_quantity DESC
LIMIT 5;


2.3.2
** Я записала запрос по ТЗ "за последний месяц" - то есть текущая дата - 1 месяц назад, но
предположу, что в реальности такие запросы для отчетов формируют за конкретный месяц (например,
если сейчас вторая половина октября, то попросили бы отчет за сентябрь)


В случае варианта запроса "топ 5 самых покупаемых продуктов за последние 30 дней":
1. Индекс по полю orders.created_at: убираем Seq Scan по orders при фильтрации WHERE
CREATE INDEX idx_orders_created_at ON orders(created_at);


В случае варианта запроса "топ 5 самых покупаемых продуктов за последний прошедший месяц":
2. Партицировние orders по дате + индекс по полю order_items.order_id: выбираем все записи orders
в файле необходимого месяца -> Index Scan по order_items 
CREATE INDEX idx_order_items_order_id ON order_items(order_id);


3. Индекс по полю order_items.product_id: убираем Seq Scan по order_items при 
order_items oi JOIN products p ON oi.product_id = p.id
CREATE INDEX idx_order_items_product_id ON order_items(product_id);


4. В таблице products добавить столбец level_one_category, в который при создании записи 
сразу сохранять categories.id категории первого уровня: решаем N+1 проблему, когда для N товаров
отправлялось N запросов к categories для определения категории первого уровня.

5. использовать MATERIALIZED VIEW с настройкой обновления данных с необходимой периодичностью

