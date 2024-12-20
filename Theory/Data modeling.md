## Методологии Kimball, Medallion и One Big Table (OBT) в хранилищах данных и аналитике

Эти методологии представляют собой различные подходы к организации, моделированию и управлению данными в хранилище данных или аналитической среде. Каждая из них имеет свои уникальные принципы, преимущества и компромиссы. Выбор подхода зависит от целей организации, объема данных и аналитических требований.

### 1. Методология Kimball
<image src="https://github.com/NikGerasimovich/Data-engineering/blob/main/Theory/IMAGE/Kimball.png" alt="Kimball">
**Обзор:**  
Методология Kimball, также известная как подход к моделированию измерений (Dimensional Modeling), направлена на проектирование хранилища данных, оптимизированного для аналитических инструментов и BI. Она предполагает "снизу-вверх" подход, при котором сначала создаются витрины данных, а затем они интегрируются в корпоративное хранилище.

**Ключевые принципы:**
- **Звёздная схема (Star Schema):**  
  Данные структурируются в таблицы фактов (количественные данные) и таблицы измерений (описательные данные). Таблицы фактов содержат числовую, измеряемую информацию (например, продажи, доходы), а таблицы измерений добавляют контекст к фактам (например, время, клиент, продукт).
- **Денормализация:**  
  Таблицы измерений денормализуются для повышения производительности запросов и упрощения отчетов. Делается акцент на простоте использования и скорости запросов, а не на эффективности хранения.
- **Витрины данных, ориентированные на предметную область:**  
  Каждая витрина данных создается вокруг конкретного бизнес-процесса или области (например, продажи, маркетинг). Витрины интегрируются в централизованное хранилище с использованием согласованных измерений.
- **Очистка и интеграция данных:**  
  Значительные усилия направляются на ETL (извлечение, преобразование, загрузка) для очистки, преобразования и интеграции данных.

**Преимущества:**
- Простота и интуитивность для бизнес-аналитиков.
- Высокая производительность запросов благодаря денормализованным структурам.
- Четкое соответствие бизнес-процессам и целям.

**Недостатки:**
- Денормализация может приводить к избыточности данных.
- Трудно масштабировать для быстро меняющихся бизнес-требований или больших наборов данных.
- Возможны проблемы с согласованностью данных при интеграции нескольких витрин.

**Примеры использования:**
- Организации, сосредоточенные на BI и отчетности.
- Среды с четко определенными бизнес-процессами и ясными требованиями к отчетности.

---

### 2. Архитектура Medallion
<image src="https://github.com/NikGerasimovich/Data-engineering/blob/main/Theory/IMAGE/medallion.png" alt="Medallion">
**Обзор:**  
Архитектура Medallion, популяризованная Databricks, представляет собой фреймворк для lakehouse, который позволяет постепенно и систематически организовывать необработанные данные и преобразовывать их в структурированную форму. Она ориентирована на масштабируемость, надежность и итеративную обработку данных.

**Ключевые принципы:**
- **Многоуровневая архитектура:**  
  - **Bronze Layer:** Сырьевые данные, поступающие из различных источников, сохраняются в неизменном виде для обеспечения достоверности.
  - **Silver Layer:** Очищенные, преобразованные и обогащенные данные, подготовленные для аналитики.
  - **Gold Layer:** Полностью агрегированные, готовые для использования бизнесом данные (например, KPI).
- **Схема при чтении (Schema-on-Read):**  
  Данные хранятся в необработанном виде, а схема применяется при запросах.
- **Инкрементальная обработка:**  
  Трансформации данных выполняются инкрементально, что позволяет плавно обновлять и интегрировать данные.

**Преимущества:**
- Гибкость при работе с разнообразными и крупномасштабными наборами данных.
- Сохранение оригинальных данных в Bronze для обеспечения трассируемости.
- Поддержка широкого спектра аналитических задач.

**Недостатки:**
- Требуется высокая квалификация инженеров данных.
- Сложность управления несколькими уровнями данных.

**Примеры использования:**
- Data Lake или Lakehouse для больших данных и BI.
- Организации, требующие масштабируемости и обработки данных в реальном времени.

---

### 3. Методология One Big Table (OBT)
<image src="https://github.com/NikGerasimovich/Data-engineering/blob/main/Theory/IMAGE/obt.png" alt="obt">
**Обзор:**  
OBT — это упрощённая, денормализованная модель данных, где вся необходимая для анализа информация объединяется в одну плоскую таблицу. Она жертвует нормализацией и избыточностью ради простоты и производительности.

**Ключевые принципы:**
- **Денормализованная структура:**  
  Все атрибуты (измерения и факты) объединяются в одну таблицу. Исключаются сложные объединения, упрощая логику запросов.
- **Предварительно обработанные данные:**  
  Данные сильно агрегируются или упрощаются для мгновенного анализа.
- **Ориентация на пользователя:**  
  Проектирование для прямого использования аналитиками и BI-инструментами.

**Преимущества:**
- Простота запросов для конечных пользователей.
- Высокая производительность для BI-инструментов.
- Минимальная кривая обучения для нетехнических пользователей.

**Недостатки:**
- Значительная избыточность данных из-за денормализации.
- Плохая масштабируемость при увеличении объемов данных.
- Трудности управления при изменении бизнес-требований.

**Примеры использования:**
- Небольшие и средние наборы данных, где важна простота.
- Среды с ограниченными техническими ресурсами.

---

### Сравнительная таблица

| Характеристика             | **Kimball**                     | **Medallion**                   | **OBT**                          |
|----------------------------|----------------------------------|----------------------------------|----------------------------------|
| **Философия**               | Моделирование измерений         | Многоуровневая обработка         | Плоская таблица                  |
| **Структура**               | Звезда/Снежинка                 | Bronze, Silver, Gold            | Одна таблица                     |
| **Обработка данных**        | ETL                              | Инкрементальное ETL/ELT         | Предварительная обработка        |
| **Гибкость**                | Умеренная                       | Высокая                         | Низкая                           |
| **Масштабируемость**        | Ограниченная                    | Высокая                         | Низкая                           |
| **Избыточность**            | Минимальная                     | Умеренная                       | Высокая                          |
| **Простота запросов**       | Умеренная                       | Умеренная/Высокая               | Очень высокая                    |
| **Производительность**      | Высокая (для отчетности)        | Высокая (распределенные системы)| Высокая для небольших данных    |

---

### Выбор подходящей методологии
- **Kimball:** Подходит для BI-систем с четко определенными процессами и относительно стабильными структурами данных.
- **Medallion:** Идеален для современных архитектур Lakehouse, поддерживающих масштабируемую аналитику.
- **OBT:** Для быстрого прототипирования или простой аналитики в условиях ограниченных ресурсов.

Каждая методология имеет свои сильные и слабые стороны. Выбор зависит от сложности данных, объема, уровня экспертизы и аналитических целей организации.
