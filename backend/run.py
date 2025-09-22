from app import create_app, db
from app.models import User, Income, Expense, Bill, Budget, Goal

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Income': Income, 'Expense': Expense, 'Bill': Bill, 'Budget': Budget, 'Goal': Goal}