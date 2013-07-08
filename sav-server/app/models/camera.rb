class Camera < ActiveRecord::Base
  validates :go_to_position, :inclusion => { :in => %w(left right hold), :message => "%{value} is not a valid position" }

  attr_accessible :url, :current_position, :current_x_position,
   :current_y_position, :go_to_position, :go_to_x_position, :go_to_y_position
end
