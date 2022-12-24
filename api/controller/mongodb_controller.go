package controller

import (
	"net/http"

	"github.com/NUTFes/nutmeg-slack/repository"
	"github.com/labstack/echo/v4"
)

type mongoDBController struct {
	repository repository.MongoDBRepository
}

type MongoDBController interface{
	IndexDocument(c echo.Context) error
}

func NewMongoDBController(repository repository.MongoDBRepository) *mongoDBController {
	return &mongoDBController{repository: repository}
}

func (controller *mongoDBController) IndexDocument(c echo.Context) error {
	doc, err := controller.repository.GetDocuments()
	if err != nil {
		panic(err)
	}
	return c.JSON(http.StatusOK, doc)
}
