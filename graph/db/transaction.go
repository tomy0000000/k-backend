package db

import (
    "fmt"
    "time"
    "gorm.io/gorm"
    "tomy0000000/k/backend/graph/model"
)

type Transaction struct {
    gorm.Model
    ID    uint64
    Timestamp time.Time `sql:"DEFAULT:current_timestamp"`
    accounts    []*PaymentAccount `gorm:"many2many:payment;"`
}

func TransactionFromGraph(t model.Transaction) Transaction {
    return Transaction{}
}

func TransactionToGraph(t Transaction) model.Transaction {
    graph := model.Transaction{ID: fmt.Sprint(t.ID)}
    return graph
}
