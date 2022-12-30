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
	IndexDocument(c echo.Context) error
	IndexChannel(c echo.Context) error
}

func NewMongoDBController(usecase usecase.MongoDBUsecase) *mongoDBController {
	return &mongoDBController{usecase: usecase}
}

func (controller *mongoDBController) IndexDocument(c echo.Context) error {
	doc := controller.usecase.GetAllCollection()
	return c.JSON(http.StatusOK, doc)
}

func (controller *mongoDBController) IndexChannel(c echo.Context) error {
	channel := controller.usecase.GetChannel()
	return c.JSON(http.StatusOK, channel)
}
