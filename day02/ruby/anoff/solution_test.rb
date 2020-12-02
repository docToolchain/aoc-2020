require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_p1
    d = {
      ['1-3 a', 'abcde'] => true,
      ['1-3 b', 'cdefg'] => false,
      ['2-9 c', 'ccccccccc'] => true
    }
    d.each { |input, valid|
      assert_equal valid, validate_password(input[1], input[0]), "Expected #{input[1]} (#{input[0]}) to be #{valid}"
    }
  end

  def test_p1
    d = {
      ['1-3 a', 'abcde'] => true,
      ['1-3 b', 'cdefg'] => false,
      ['2-9 c', 'ccccccccc'] => false
    }
    d.each { |input, valid|
      assert_equal valid, validate_password2(input[1], input[0]), "Expected #{input[1]} (#{input[0]}) to be #{valid}"
    }
  end
end