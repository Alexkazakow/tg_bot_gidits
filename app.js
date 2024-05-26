let tg = window.Telegram.WebApp;

// tg.expand();
tg.MainButton.show();
tg.MainButton.setText("Закрыть");



Telegram.WebApp.onEvent("mainButtonClicked", function(){
	tg.close();
});

// Эта функция используется для добавления конкретного "value" (значения) на дисплей.
function addToDisplay(value) {
document.getElementById('display').value += value;
}
// Эта функция очищает дисплей, устанавливая его значение в пустую строку.
function clearDisplay() {
document.getElementById('display').value = '';
document.getElementById("result").innerText = 'Result: ';
}
// Эта функция вычисляет результат выражения на дисплее с помощью функции 'eval'.
// Она обрабатывает ошибки и выводит сообщение 'Error', если выражение недопустимо.
function calculateResult() {
try {
// Получение результата выражения и вывод результата на дисплей.
    document.getElementById("result").innerText = "Result: " + eval(document.getElementById('display').value);
    // document.getElementById('display').value = eval(document.getElementById('display').value);
} catch (error) {
// Если в процессе вычисления возникла ошибка, на дисплее отобразится сообщение 'Error'.
    document.getElementById('display').value = 'Error';
}
}