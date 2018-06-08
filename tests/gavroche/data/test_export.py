from valjean.gavroche.harvest import export


@export('test_with_name')
def do_stuff():
    pass


#without explicit name
@export
def test_some_stuff():
    pass
del test_some_stuff


@export('does_not_start_with_test')
def do_something():
    pass


# export in loop
for i in range(3):
    @export('test_loop_{}'.format(i))
    def in_loop():
        pass
