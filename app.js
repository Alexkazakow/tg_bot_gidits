let tg = window.Telegram.WebApp;

// tg.expand();
tg.MainButton.show();
tg.MainButton.setText("Закрыть");



Telegram.WebApp.onEvent("mainButtonClicked", function(){
	tg.close();
});