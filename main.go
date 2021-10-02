package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

var (
	URL           = "https://www.vikacg.com/wp-json/b2/v1/userMission"
	AUTHORIZATION = os.Getenv("secrets.AUTHORIZATION")
	COOKIE        = os.Getenv("secrets.COOKIE")
)

type checkResult struct {
	Credit  int     `json:"credit"`
	Mission mission `json:"mission"`
}

type mission struct {
	MyCredit string `json:"my_credit"`
}

func main() {

	if AUTHORIZATION == "" || COOKIE == "" {
		log.Print("no configuration was read, please check the configuration")
		return
	}

	authorizationArray := strings.Split(AUTHORIZATION, "#")
	cookieArray := strings.Split(COOKIE, "#")

	length := len(authorizationArray)
	if length != len(cookieArray) {
		log.Print("wrong configuration was read, please check the configuration")
		return
	}

	for i := 0; i < length; i++ {
		log.Printf("正在签到第%d个用户, 共计%d个用户", i+1, length)
		check(authorizationArray[i], cookieArray[i])
	}
}

func check(authorization, cookie string) {
	request, err := http.NewRequest(http.MethodPost, URL, nil)
	if err != nil {
		log.Print(err)
		return
	}

	request.Header.Add("authorization", authorization)
	request.Header.Add("cookie", cookie)

	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		log.Print(err)
		return
	}

	bytes, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Print(err)
		return
	}

	if response.StatusCode != http.StatusOK {
		log.Print(string(bytes))
		return
	}

	data := new(checkResult)
	err = json.Unmarshal(bytes, &data)
	if err != nil {
		log.Printf("今日已经签到过, 已经获得过积分%s分", strings.Trim(string(bytes), `"`))
		return
	}

	log.Printf("签到成功, 获得积分%d分, 目前总积分%s分", data.Credit, data.Mission.MyCredit)
}
