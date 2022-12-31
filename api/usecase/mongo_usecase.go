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

func NewMongoDBUsecase(r repository.MongoDBRepository) *mongoDBUsecase {
	return &mongoDBUsecase{repository: r}
}

func (u *mongoDBUsecase) GetAllCollection() (docs []bson.M) {
	docs, err := u.repository.AllCollection()
	if err != nil {
		panic(err)
	}
	return docs
}

func (u *mongoDBUsecase) GetChannel() []string {
	docs, err := u.repository.AllCollection()
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
