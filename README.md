# Miramar Ticket Bot - 美麗華大直IMAX影城訂票機器人

## 簡介

此程式可以協助你購買美麗華大直IMAX影城的電影票，透過自動化的程序，實現快速選擇場次、票種、場次日期時間的功能。

作者LD於2023年7月底一時興起開發此程式，為了觀看台灣最高規格的IMAX奧本海默...

## 使用方法

1. 從 [這裡](https://github.com/HappyGroupHub/MiramarTicketBot/releases) 下載最新版本的程式
2. 解壓縮檔案後會生成一個資料夾
3. 打開 `config.yml` 並完成填寫裡面的資料 (詳細說明請看下面介紹)
4. 開啟 `MiramarTicketBot.exe` 完成登入後，等待選位流程完成即可

## 關於 config.yml

```yaml
# ++--------------------------------++
# | MiramarTicketBot                 |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# NOTES:
# If any ding sound is played while the program running
# It means that there's a manual action is required.


# Login information
# Note that you have to finish the captcha manually.
email: ''
password: ''

# Tickets date and time
# Enter the date and time you want to book.
date: '8/3'
time: '23:10'

# Tickets selection
# Please enter the amount of ticket you want to book.
imax_adults: 2
imax_students: 0
imax_seniors: 0
imax_disabled: 0

# Seat selection
# Please enter the seat you want to book.
seats:
  - 'G23'
  - 'G24'
  
# Invoice settings (optional)
# Invoice number should start with / and contains 7 character behind.
# Example: /A123456
invoice: ''

# Headless mode
# If you want to run this script in headless mode, please set this to true.
headless: false

```

* `email`: 請填入你的美麗華會員帳號
* `password`: 請填入你的美麗華會員密碼
* `date`: 請填入你想要訂票的日期，格式為 `M/D`，例如 `8/3`
* `time`: 請填入你想要訂票的場次時間，格式為 `HH:MM`，例如 `23:10`
* `imax_adults`: 請填入你想要訂購的成人票數量
* `imax_students`: 請填入你想要訂購的學生、軍警票票數量
* `imax_seniors`: 請填入你想要訂購的敬老票數量
* `imax_disabled`: 請填入你想要訂購的身障票數量
* `seats`: 請填入你想要訂購的座位，數量必須與上面的票種總數相同
* `invoice`: (選填) 請填入你的發票載具，格式為 `/` 加上 7 個字元，例如 `/A123456`
* `headless`: 如果你想要在背景執行，請填入 `true`，否則請填入 `false`

## 常見問題

### Q1: 為什麼我會聽到 叮~ 的聲音？

A: 若你在程式運行中聽到此聲音，代表你需要手動完成一些動作，例如完成驗證測驗、選擇座位場次等等，程式完成搶位後也會出現此聲音提醒你喔!

### Q2: 為什麼我有時候要重新登入，有時候不用？

A: 美麗華影城的登入機制有時效性，我們雖然會儲存你的cookies讓你下次不必再重新登入，但一旦cookies過期，你就必須重新登入。

### Q3: 我無法在此瀏覽器上完成驗證測驗，怎麼辦？

A: 如果你在登入時無法完成驗證測驗，你可以在自己本機其他瀏覽器上完成登入，然後將cookies內的兩特定值複製到`cookies.json`，這樣就可以了。

## 遇到任何問題嗎?

如果你在使用上面有遇到任何問題或bug，甚至是有建議想提出，請到 [這裡](https://github.com/HappyGroupHub/MiramarTicketBot/issues) 提出你的想法!

## 版權

此專案的版權規範採用 MIT License - 至 [LICENSE](LICENSE) 查看更多相關聲明