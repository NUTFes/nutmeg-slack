package usecase

import (
	"github.com/NUTFes/nutmeg-slack/repository"
	"github.com/NUTFes/nutmeg-slack/usecase/util"
	"go.mongodb.org/mongo-driver/bson"
)

type mongoDBUsecase struct {
	repository repository.MongoDBRepository
}

type MongoDBUsecase interface {
	GetAllCollection() []bson.M
	GetChannel() []string
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

func (usecase *mongoDBUsecase) GetChannel() []string {
	docs, err := usecase.repository.AllCollection()
	var channelSlice []string
	for _, v := range docs {
		// channelにvを格納する
		channel := v["event"].(bson.M)["channel"].(string)
		if util.Iscontains(channelSlice, channel) == false {
			channelSlice = append(channelSlice, channel)
		}
	}
	if err != nil {
		panic(err)
	}
	return channelSlice
}
