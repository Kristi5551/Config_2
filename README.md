### Config_2

Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление PlantUML. Визуализатор должен выводить результат на экран в виде кода графа.

---

Построить граф зависимостей для коммитов, в узлах которого содержатся дата, время и автор коммита. Граф необходимо строить только для тех коммитов, где фигурирует файл с заданным именем.

---

Ключами командной строки задаются:
- Путь к программе для визуализации графов.
- Путь к анализируемому репозиторию.
- Файл с заданным именем в репозитории.

---

Программа была протестирована успешно.
![photo_2024-12-20_16-07-40](https://github.com/user-attachments/assets/76a78147-4480-4b07-b983-dc9accf7c57d)
