package controller

import (
	"net/http"

	"github.com/NUTFes/nutmeg-slack/usecase"
	"github.com/labstack/echo/v4"
)

type mongoDBController struct {
	usecase usecase.MongoDBUsecase
}

type MongoDBController interface {
	IndexDocument(ctx echo.Context) error
	IndexChannel(ctx echo.Context) error
	IndexData(ctx echo.Context) error
}

func NewMongoDBController(u usecase.MongoDBUsecase) *mongoDBController {
	return &mongoDBController{usecase: u}
}

func (c *mongoDBController) IndexDocument(ctx echo.Context) error {
	doc := c.usecase.GetAllCollection()
	return ctx.JSON(http.StatusOK, doc)
}

func (c *mongoDBController) IndexChannel(ctx echo.Context) error {
	channel := c.usecase.GetChannel()
	return ctx.JSON(http.StatusOK, channel)
}

func (c *mongoDBController) IndexData(ctx echo.Context) error {
	user := c.usecase.FetchData()
	return ctx.JSON(http.StatusOK, user)
}
