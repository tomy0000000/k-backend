package graph

//go:generate go run github.com/99designs/gqlgen

// This file will not be regenerated automatically.
//
// It serves as dependency injection for your app, add any dependencies you require here.

import (
    "tomy0000000/k/backend/graph/model"
    "gorm.io/gorm"
)

type Resolver struct {
    DB *gorm.DB
    todos []*model.Todo
}
