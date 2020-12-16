import pytest



  
def test_read():
    from util import read_file_to_list
    from util import scanning
    fields, tickets = read_file_to_list('testinput.txt')
    
    assert 3 == len(fields)
    assert 5 == len(tickets)
    assert 3 == len(tickets[0])

    error_rate, positions = scanning(fields, tickets)
    assert 71 == error_rate
    assert positions[0] == {'row'}
    assert positions[1] == {'class'}
    assert positions[2] == {'seat'}


   