import pytest

##### Es werden alle möglichen Übergabeparameter registert und ggf. mit Default-Werten versehen.
def pytest_addoption(parser):
	parser.addoption("--tests", action="store", default="", help="Liste für Testskripte: ;-separiert")
	parser.addoption("--zielordner", action="store", default="F:/Testresultate/", help="Zielordner zur Ablage der Testergebnisse")
	parser.addoption("--headless", action="store", default="1", help="Headless Modus: 1-Ja 0-Nein")
	parser.addoption("--browser", action="store", default="Chrome", help="Browser: Chrome,FF")
	parser.addoption("--url", action="store", default="https://navtst.soka-dach.de/DynamicsNAV_TST/", help="URL: Zieladresse für Testbeginn")
	parser.addoption("--loglvl", action="store", default="1", help="Umfang der Testdokumentation")
	parser.addoption("--folder", action="store", default="", help="Ordner der Testfallabläufe (*.tc Dateien) enthält. Die Testliste wird dynamisch gebildet")
	parser.addoption("--subfolder", action="store", default="0", help="Gibt an, ob Unterordner einbezogen werden sollen, bei der Testfalllistenerstellung")
	parser.addoption("--jobname", action="store", default="Übersicht", help="Dateiname der Testlauf-Übersichtsdatei")
	parser.addoption("--testliste", action="store", default="", help="Ein Textfile mit Zeilenweise getrennten Testfällen kann übergeben werden")

@pytest.fixture
def config_param(request):
	#return request.config.getoption("--tests")
	config_param = {}
	config_param["tests"] = request.config.getoption("--tests")
	config_param["zielordner"] = request.config.getoption("--zielordner")
	config_param["headless"] = request.config.getoption("--headless")
	config_param["browser"] = request.config.getoption("--browser")
	config_param["url"] = request.config.getoption("--url")
	config_param["loglvl"] = request.config.getoption("--loglvl")
	config_param["folder"] = request.config.getoption("--folder")
	config_param["jobname"] = request.config.getoption("--jobname")
	config_param["subfolder"] = request.config.getoption("--subfolder")
	config_param["testliste"] = request.config.getoption("--testliste")
	return config_param