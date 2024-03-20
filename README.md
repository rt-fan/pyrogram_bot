# pyrogram_bot

ТЗ Воронка-вебинар
Время	- 6min | 39min | 1 day 2 hours
Текст - Текст1 | Текст2 | Текст3
Точка отсчёта - Первое сообщение клиента | Время отправки сообщения msg_1 | Время отправки сообщения msg_2 или время, когда оно было отменено (найден триггер)
Триггеры на отмену отправки - x |Триггер1 (это просто слово) | x
Сообщения пользователя - msg_1 | msg_2 | msg_3

---

Примечание: перед отправкой каждого сообщения проверять на наличие слов: ("прекрасно" | ИЛИ | "ожидать"). Если были найдены, то вся воронка прекращается. Задание -- юзербот! Не путать с aiogram\telebot и тд ТГ ботами

---

**Стек:** ЯП: python

**Модули:** pyrogram, sqlalchemy (asynpg)

---

**! Не использовать механики scheduler.**

Должна быть while True задача, которая для каждого сообщения проверяет ""готовых для получения сообщения"" пользователей."

---

**Обязательные столбцы БД:**

"id # ID пользователя

created_at # Время ""регистарции в воронку""

status # alive | dead | finished

status_updated_at  # Когда был обновлён столбец status

---

**Объяснение по статусам:**

alive --- по умолчанию, получаем только таких пользователей

dead --- если получили ошибки при отправке\проверке триггеров например: BotBlocked, UserDeactivated

finished --- конец воронки"			
						
						
						
						
*Триггер -- в данном случае слово или фраза, найденная в каком-либо сообщении от нашего аккаунта (автоответчика), вызывающая такое-то действие. В данном случае: либо отмену отправки сообщения и переход к следующему, либо (если прекрасно\ожидать) окончание воронки

*Точка отсчёта -- в данном случае время, когда произошло такое-то событие. То есть отправить такой-то текст через Х "Время" от Y события						
