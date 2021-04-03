package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"math/rand"
	"tomy0000000/kman/k-graphql/graph/db"
	"tomy0000000/kman/k-graphql/graph/generated"
	"tomy0000000/kman/k-graphql/graph/model"
)

func (r *mutationResolver) CreateTodo(ctx context.Context, input model.NewTodo) (*model.Todo, error) {
	todo := &model.Todo{
		Text:   input.Text,
		ID:     fmt.Sprintf("T%d", rand.Int()),
		UserID: input.UserID,
	}
	r.todos = append(r.todos, todo)
	return todo, nil
}

func (r *mutationResolver) CreatePaymentAccount(ctx context.Context, input model.NewPaymentAccount) (*model.PaymentAccount, error) {
	var account = &model.PaymentAccount{
		Name: input.Name,
	}
	db_account := db.PaymentAccountFromGraph(*account)
	r.DB.Create(&db_account)
	account.ID = fmt.Sprint(db_account.ID)
	return account, nil
}

func (r *queryResolver) Todos(ctx context.Context) ([]*model.Todo, error) {
	return r.todos, nil
}

func (r *queryResolver) PaymentAccount(ctx context.Context) ([]*model.PaymentAccount, error) {
	var db_accounts []db.PaymentAccount
	var accounts []*model.PaymentAccount
	result := r.DB.Find(&db_accounts)
	if result.Error != nil {
		panic("failed to query PaymentAccount")
	}
	for _, db_account := range db_accounts {
		tmp_account := db.PaymentAccountToGraph(db_account)
		accounts = append(accounts, &tmp_account)
	}
	return accounts, nil
}

func (r *todoResolver) User(ctx context.Context, obj *model.Todo) (*model.User, error) {
	return &model.User{ID: obj.UserID, Name: "user " + obj.UserID}, nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

// Todo returns generated.TodoResolver implementation.
func (r *Resolver) Todo() generated.TodoResolver { return &todoResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
type todoResolver struct{ *Resolver }
