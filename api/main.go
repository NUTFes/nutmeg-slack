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

	// CORS
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		// TODO: 本番環境のURLも許可する
		AllowOrigins: []string{"http://localhost:8080"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
	}))
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.Logger.Fatal(e.Start(":1323"))
}
