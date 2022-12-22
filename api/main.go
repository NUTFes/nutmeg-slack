package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	e := echo.New()

	ConnectMongo()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", hello)

	e.Logger.Fatal(e.Start(":1323"))
}

func hello(c echo.Context) error {
	return c.String(http.StatusOK, "Hello, World")
}

func ConnectMongo() *mongo.Client {
	credential := options.Credential{
		Username: "root",
		Password: "password",
	}
	clientOptions := options.Client().ApplyURI("mongodb://mongo").SetAuth(credential)
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		panic(err)
	} else {
		fmt.Println("Connected to MongoDB!")
	}

	// col, err := client.Database("nutfes_slack_log_dev").Collection("log").Find(context.Background(), bson.M{})
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// var result []bson.M
	// if err = col.All(context.Background(), &result); err != nil {
	// 	log.Fatal(err)
	// }
	// for _, item := range result {
	// 	fmt.Println(item)
	// }

	fmt.Println(col)
	return client
}
