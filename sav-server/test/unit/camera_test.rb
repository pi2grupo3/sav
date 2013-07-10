require 'test_helper'

class CameraTest < ActiveSupport::TestCase
 
  test "translade to right" do
    cam = Camera.create!(:current_position => 0, :go_to_position => "right")
    cam.translade
    assert_equal 1, cam.current_position
  end  
end
