class Camera < ActiveRecord::Base
  #TODO add unit test to this class
  CHECKPOINT_NUMBER = 3

  validates :go_to_position, :inclusion => { :in => %w(left right hold),
	:message => "%{value} is not a valid command" }

  validates :current_position, :inclusion => { :in => 0...CHECKPOINT_NUMBER,
	:message => "%{value} is not a valid position" }

  attr_accessible :url, :description, :current_position, :current_x_position,
   :current_y_position, :go_to_position, :go_to_x_position, :go_to_y_position

  def checkpoints
	CHECKPOINT_NUMBER
  end

  #Adds 1 to current_position for presentation
  def show_current_position
    self.current_position + 1
  end

  def can_go?(side)
	  unless side == 'hold'
      self.send("can_go_#{side.gsub("?", "")}?")
	  end
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
    if self.current_position >= (CHECKPOINT_NUMBER - 1)
	    false
    else
	    true
    end
  end

	#updates position based on previous direction
	def update_position
		if self.go_to_position == 'right'
			self.current_position += 1 unless self.current_position >= CHECKPOINT_NUMBER
		elsif self.go_to_position == 'left'
			self.current_position += 1 unless self.current_position <= CHECKPOINT_NUMBER
		end
	end
end
