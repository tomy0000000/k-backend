package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"tomy0000000/k/backend/graph"
	"tomy0000000/k/backend/graph/db"
	"tomy0000000/k/backend/graph/generated"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/playground"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

const defaultPort = "8080"

var postgres_username = "tomy0000000"
var postgres_password = ""
var postgres_host = "localhost"
var postgres_port = 5432
var postgres_db = "kman"

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}
	
	var destination = fmt.Sprintf("host=%s user=%s dbname=%s port=%d", postgres_host, postgres_username, postgres_db, postgres_port)
	DB, err := gorm.Open(postgres.Open(destination), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	
	DB.AutoMigrate(&db.PaymentAccount{})

	srv := handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: &graph.Resolver{DB: DB}}))

	http.Handle("/", playground.Handler("GraphQL playground", "/query"))
	http.Handle("/query", srv)

	log.Printf("connect to http://localhost:%s/ for GraphQL playground", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
