# Lambda, Kappa и Delta архитектуры

## 1. Lambda Architecture
**Lambda Architecture** была предложена для обработки больших данных в режиме реального времени и пакетной обработки. Она ориентирована на обеспечение надежности, масштабируемости и минимальной задержки для аналитики.

### Компоненты Lambda Architecture
#### Batch Layer (Пакетная обработка)
- Сохраняет полный источник данных в неизменяемом формате (Data Lake или HDFS).
- Выполняет сложные вычисления и пересчёты на основе всей доступной информации.
- Использует MapReduce или Spark для обработки больших объёмов данных.

#### Speed Layer (Обработка в реальном времени)
- Обрабатывает только поступающие данные в реальном времени, предоставляя результаты с низкой задержкой.
- Используются стриминговые системы, такие как Apache Kafka, Apache Flink или Apache Storm.

#### Serving Layer (Слой доступа)
- Объединяет результаты из Batch и Speed слоёв для предоставления конечных аналитических данных.
- Использует базы данных, оптимизированные для чтения (например, Cassandra, Elasticsearch).

### Преимущества Lambda Architecture
- **Гибкость**: Подходит для аналитики в режиме реального времени и сложной пакетной обработки.
- **Надежность**: Обеспечивает корректные результаты даже при сбоях в одном из слоёв.
- **Масштабируемость**: Легко масштабируется как в пакетной, так и в стриминговой обработке.

### Недостатки Lambda Architecture
- **Сложность**: Требуется дублировать код для Speed и Batch слоёв, что затрудняет поддержку.
- **Задержка**: Хотя Speed Layer даёт результаты быстро, корректные данные появляются только после обработки в Batch Layer.
- **Высокие затраты**: Нужны отдельные ресурсы для каждого слоя.
<image src="https://github.com/NikGerasimovich/Data-engineering/blob/main/Theory/IMAGE/kappa.webp" alt="kappa">
---

## 2. Kappa Architecture
**Kappa Architecture** предложена как упрощение Lambda, ориентированное на стриминговую обработку данных.

### Основные принципы Kappa Architecture
#### Stream-Only Model (Только стриминг)
- Все данные обрабатываются через стриминговую систему.
- Нет разделения на Batch и Speed слои.

#### Хранение данных
- Источник данных, как правило, хранится в неизменяемом виде в системе, поддерживающей стриминг, например, Apache Kafka.
- Новые вычисления или преобразования выполняются поверх данных, повторяя поток при необходимости.

#### Обработка
- Используются системы, оптимизированные для потоковой обработки, такие как Apache Flink, Apache Kafka Streams или Apache Pulsar.

### Преимущества Kappa Architecture
- **Простота**: Нет дублирования логики, так как используется единая система для обработки.
- **Реальная скорость**: Отлично подходит для систем, где данные обрабатываются в реальном времени.
- **Гибкость для изменений**: Пересчёт выполняется путём повторного запуска потока.

### Недостатки Kappa Architecture
- **Меньшая универсальность**: Не так удобна для сложных аналитических задач, требующих пакетной обработки.
- **Требовательность к инфраструктуре**: Для обеспечения надёжности в реальном времени нужны мощные стриминговые платформы.
- **Ограничения обработки**: Некоторые аналитические задачи сложнее реализовать только в стриминговом режиме.
<image src="https://github.com/NikGerasimovich/Data-engineering/blob/main/Theory/IMAGE/Lamda.jpg" alt="lambda">
---

## 3. Delta Architecture
**Delta Architecture** разработана для устранения недостатков Lambda и Kappa. Это подход, основанный на объединении обработки потоков и пакетов с использованием транзакционных хранилищ данных, таких как Delta Lake.

### Основные принципы Delta Architecture
#### Единое хранилище данных
- Используется ACID-хранилище (например, Delta Lake, Apache Hudi или Apache Iceberg).
- Все данные хранятся в одном месте, как потоковые, так и пакетные.

#### Гибридная обработка (Stream-Batch Processing)
- Потоковые данные сначала записываются в Delta Lake, а затем обрабатываются как пакетные.
- Исторические данные и потоковые события объединяются в одной системе.

#### Обработка данных
- Потоковая обработка осуществляется системами, такими как Apache Spark Structured Streaming.
- Исторические запросы выполняются напрямую из Delta Lake.

### Преимущества Delta Architecture
- **Упрощённая архитектура**: Нет необходимости поддерживать несколько слоёв.
- **ACID-гарантии**: Хранилище поддерживает транзакционность и консистентность данных.
- **Универсальность**: Подходит как для потоковой, так и для пакетной обработки.
- **Эффективное управление данными**: Поддержка версионности и упрощённый пересчёт данных.

### Недостатки Delta Architecture
- **Зависимость от платформы**: Требует использования хранилищ с поддержкой ACID.
- **Сложность внедрения**: Может потребовать переработки существующей инфраструктуры.
- **Ограничения в стриминговой обработке**: Скорость обработки может быть ниже, чем у чисто стриминговых архитектур.

---

## 4. Сравнение Lambda, Kappa и Delta Architectures

| Характеристика               | Lambda                          | Kappa                          | Delta                          |
|------------------------------|----------------------------------|--------------------------------|--------------------------------|
| **Обработка**               | Пакетная и потоковая             | Только потоковая               | Гибридная (Stream-Batch)       |
| **Хранилище данных**        | Раздельное                      | Неизменяемое потоковое         | ACID-хранилище                 |
| **Сложность**               | Высокая                         | Низкая                         | Умеренная                      |
| **Скорость обработки**      | Умеренная                       | Высокая                        | Умеренная                      |
| **Гарантия консистентности**| Зависит от реализации           | Зависит от реализации          | ACID                           |
| **Тип задач**               | Реальное время + аналитика       | Реальное время                 | Универсальная аналитика        |

---

## 5. Рекомендации по выбору архитектуры

### Lambda Architecture
Используйте, если:
- Требуется обработка как в реальном времени, так и пакетная аналитика.
- Необходимы надёжность и масштабируемость.
- Допустимы сложность и дублирование кода.

### Kappa Architecture
Используйте, если:
- Основной фокус — обработка данных в реальном времени.
- Нет необходимости в сложной пакетной аналитике.
- Требуется простота архитектуры.

### Delta Architecture
Используйте, если:
- Необходим единый подход для потоковой и пакетной обработки.
- Требуются транзакционные гарантии и высокая консистентность данных.
- Вы хотите минимизировать сложность архитектуры.

---

## 6. Выводы
- **Lambda Architecture** остаётся подходящим выбором для сложных сценариев, где требуется сочетание реального времени и глубокой аналитики.
- **Kappa Architecture** лучше всего подходит для систем реального времени с минимальной задержкой.
- **Delta Architecture** предлагает универсальность, упрощённость и ACID-гарантии, что делает её идеальной для современных Data Lake и Data Warehouse систем.

Ваш выбор должен основываться на особенностях вашего проекта, требуемой производительности, сложности внедрения и поддержания.