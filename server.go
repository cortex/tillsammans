package main

import (
	"net/http"

	"github.com/gorilla/context"
	"github.com/keep94/weblogs"
)

func users(w http.ResponseWriter, r *http.Request) {
}

func tasks(w http.ResponseWriter, r *http.Request) {

}

func main() {
	http.HandleFunc("/users", users)
	http.HandleFunc("/tasks", tasks)
	handler := context.ClearHandler(weblogs.Handler(http.DefaultServeMux))
	http.ListenAndServe("8080", handler)
}
