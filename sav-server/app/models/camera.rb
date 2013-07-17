class Camera < ActiveRecord::Base
  #TODO add unit test to this class

  validates :go_to_position, :inclusion => { :in => %w(left right hold),
	:message => "%{value} is not a valid position" }

  attr_accessible :url, :current_position, :current_x_position,
   :current_y_position, :go_to_position, :go_to_x_position, :go_to_y_position

  CHECKPOINT_NUMBERS = 3

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

  def can_go(side)
    self.send("can_go_#{side.gsub("?", ""}?")
  end

  #checks if the camera can go left
  def can_go_left?
    if self.current_position <= 0
	false
    else
	true
    end
  end

   #checks if the camera can go right
  def can_go_right?
    if self.current_position >= (CHECKPOINT_NUMBERS - 1)
	false
    else
	true
    end
  end
end
