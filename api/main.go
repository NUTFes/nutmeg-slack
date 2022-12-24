package main

import (
	"github.com/NUTFes/nutmeg-slack/controller"
	"github.com/NUTFes/nutmeg-slack/db"
	"github.com/NUTFes/nutmeg-slack/repository"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	e := echo.New()
	client := db.ConnectMongo()
	repository := repository.NewMongoDBRepository(client)
	controller := controller.NewMongoDBController(repository)

	e.GET("/documents", controller.IndexDocument)

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.Logger.Fatal(e.Start(":1323"))
}
