package usecase

import (
	"fmt"

	"github.com/NUTFes/nutmeg-slack/repository"
	"go.mongodb.org/mongo-driver/bson"
)

type mongoDBUsecase struct {
	repository repository.MongoDBRepository
}

type MongoDBUsecase interface {
	GetAllCollection() []bson.M
	GetChannel() []map[string]string
}

func NewMongoDBUsecase(repository repository.MongoDBRepository) *mongoDBUsecase {
	return &mongoDBUsecase{repository: repository}
}

func (usecase *mongoDBUsecase) GetAllCollection() (docs []bson.M) {
	docs, err := usecase.repository.AllCollection()
	if err != nil {
		panic(err)
	}
	return docs
}

func (usecase *mongoDBUsecase) GetChannel() (channel []map[string]string) {
	docs, err := usecase.repository.AllCollection()
	for _, v := range docs {
		a := v["event"].(bson.M)["channel"]
		b := make(map[string]string)
		b["channel"] = a.(string)
		channel = append(channel, b)
	}
	fmt.Println(channel)
	if err != nil {
		panic(err)
	}
	return channel
}
