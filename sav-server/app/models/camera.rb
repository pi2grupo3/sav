class Camera < ActiveRecord::Base
  validates :go_to_position, :inclusion => { :in => %w(left right hold), :message => "%{value} is not a valid position" }

  attr_accessible :url, :current_position, :current_x_position,
   :current_y_position, :go_to_position, :go_to_x_position, :go_to_y_position

  #update position when translading...
  def translade
    direction = self.go_to_position
    if direction == "left"
      self.current_position -= 1
    elsif direction == "right"
      self.current_position += 1
    end
    self.go_to_position = "hold"
    self.save    
  end
end
