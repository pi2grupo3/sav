class Camera < ActiveRecord::Base
  attr_accessible :batery_state, :current_position, :current_x_position, :current_y_position, :go_to_position, :go_to_x_position, :go_to_y_position
end
