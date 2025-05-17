import ui
import app
import net
import chat

class StakeWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.selectedOption = None
		self.__LoadWindow()
		self.Hide()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(440, 350)
		self.Board.SetCenterPosition()
		self.Board.SetTitleName("Stake Seçenekleri")
		self.Board.Show()

		self.CreateOptionBox("Günlük", "1 EP / M / Gün", 30, "daily")
		self.CreateOptionBox("Haftalık", "2 EP / M / Gün", 160, "weekly")
		self.CreateOptionBox("Aylık", "3 EP / M / Gün", 290, "monthly")

		self.infoText = ui.TextLine()
		self.infoText.SetParent(self.Board)
		self.infoText.SetPosition(30, 200)
		self.infoText.SetText("Sadece tam Milyon (1M, 2M, vb.) girilebilir.")
		self.infoText.Show()

		self.inputBackground = ui.Bar()
		self.inputBackground.SetParent(self.Board)
		self.inputBackground.SetPosition(30, 225)
		self.inputBackground.SetSize(250, 20)
		self.inputBackground.SetColor(0xFF000000)
		self.inputBackground.Show()

		self.yangInput = ui.EditLine()
		self.yangInput.SetParent(self.inputBackground)
		self.yangInput.SetSize(240, 18)
		self.yangInput.SetPosition(5, 1)
		self.yangInput.SetMax(12)
		self.yangInput.SetText("1000000")
		self.yangInput.SetFontColor(1.0, 1.0, 1.0)
		self.yangInput.Show()

		self.stakeButton = ui.Button()
		self.stakeButton.SetParent(self.Board)
		self.stakeButton.SetPosition(290, 223)
		self.stakeButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.stakeButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.stakeButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.stakeButton.SetText("Stake")
		self.stakeButton.SetEvent(self.OnClickStake)
		self.stakeButton.Show()

		self.viewStakeButton = ui.Button()
		self.viewStakeButton.SetParent(self.Board)
		self.viewStakeButton.SetPosition(130, 270)
		self.viewStakeButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.viewStakeButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.viewStakeButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.viewStakeButton.SetText("Aktif Stake İşlemlerin")
		self.viewStakeButton.SetEvent(self.OnClickViewStakes)
		self.viewStakeButton.Show()

	def CreateOptionBox(self, title, desc, posX, optionKey):
		bg = ui.ThinBoard()
		bg.SetParent(self.Board)
		bg.SetSize(120, 70)
		bg.SetPosition(posX, 50)
		bg.Show()

		titleText = ui.TextLine()
		titleText.SetParent(bg)
		titleText.SetPosition(60, 10)
		titleText.SetHorizontalAlignCenter()
		titleText.SetText(title)
		titleText.Show()

		descText = ui.TextLine()
		descText.SetParent(bg)
		descText.SetPosition(60, 30)
		descText.SetHorizontalAlignCenter()
		descText.SetText(desc)
		descText.Show()

		btn = ui.Button()
		btn.SetParent(bg)
		btn.SetPosition(25, 45)
		btn.SetUpVisual("d:/ymir work/ui/public/small_Button_01.sub")
		btn.SetOverVisual("d:/ymir work/ui/public/small_Button_02.sub")
		btn.SetDownVisual("d:/ymir work/ui/public/small_Button_03.sub")
		btn.SetText("Seç")
		btn.SetEvent(lambda: self.SelectOption(optionKey))
		btn.Show()

	def SelectOption(self, option):
		self.selectedOption = option
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Seçim yapıldı: %s" % self.selectedOption)

	def OnClickStake(self):
		if not self.selectedOption:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Lütfen bir stake süresi seçin.")
			return

		yang_str = self.yangInput.GetText()
		try:
			yang = int(yang_str)
			if yang < 1000000 or yang % 1000000 != 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Sadece 1M ve katları girilebilir.")
				return

			net.SendChatPacket("/stakeyang %d %s" % (yang, self.selectedOption))
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%d Yang stake edildi. Seçim: %s." % (yang, self.selectedOption))
			self.Close()
		except ValueError:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Sayı girmelisin.")

	def OnClickViewStakes(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Aktif stake işlemlerinizi görmek için henüz sistem hazır değil.")

	def Close(self):
		self.Hide()