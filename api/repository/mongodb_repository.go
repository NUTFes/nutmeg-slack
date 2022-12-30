package repository

import (
	"context"
	"log"

	"github.com/NUTFes/nutmeg-slack/db"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type mongoDBRepository struct {
	client *mongo.Client
}

type MongoDBRepository interface {
	AllCollection() ([]bson.M, error)
}

func NewMongoDBRepository(client *mongo.Client) *mongoDBRepository {
	return &mongoDBRepository{client: client}
}

func (mongoDBRepository) AllCollection() ([]bson.M, error) {
	client := db.ConnectMongo()
	col, err := client.Database("nutfes_slack_log_dev").Collection("log").Find(context.Background(), bson.M{})
	if err != nil {
		log.Fatal(err)
	}
	var result []bson.M
	if err = col.All(context.Background(), &result); err != nil {
		log.Fatal(err)
	}
	return result, nil
}
