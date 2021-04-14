package db

import (
    "fmt"
    "gorm.io/gorm"
    "tomy0000000/k/backend/graph/model"
)

type Item struct {
    gorm.Model
    ID    uint32
    Name    string
}

func ItemFromGraph(i model.Item) Item {
    return Item{Name: i.Name}
}

func ItemToGraph(i Item) model.Item {
    graph := model.Item{ID: fmt.Sprint(i.ID), Name: i.Name}
    return graph
}
