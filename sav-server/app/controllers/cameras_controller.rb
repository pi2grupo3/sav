class CamerasController < ApplicationController
  # GET /cameras
  # GET /cameras.json
before_filter :authenticate_user!

  def index
    @cameras = Camera.all

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @cameras }
    end
  end

  # GET /cameras/1
  # GET /cameras/1.json
  def show
    @camera = Camera.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
	  format.js
      format.json { render json: @camera }
    end
  end

  # GET /cameras/new
  # GET /cameras/new.json
  def new
    @camera = Camera.new

    respond_to do |format|
      format.html # new.html.erb
      format.json { render json: @camera }
    end
  end

  # GET /cameras/1/edit
  def edit
    @camera = Camera.find(params[:id])
  end

  # POST /cameras
  # POST /cameras.json
  def create
    @camera = Camera.new(params[:camera])

		if params[:camera][:url].nil? || params[:camera][:url].empty?
			@camera.url = 'SAV_StreamOff.png'
		end
		if params[:camera][:current_position].nil?
			@camera.current_position = 0
		end
		if params[:camera][:go_to_position].nil?
			@camera.go_to_position = 'hold'
		end
    	

    respond_to do |format|
      if @camera.save
        format.html { redirect_to @camera, notice: 'Camera was successfully created.' }
        format.json { render json: @camera, status: :created, location: @camera }
      else
        format.html { render action: "new" }
        format.json { render json: @camera.errors, status: :unprocessable_entity }
      end
    end
  end

  # PUT /cameras/1
  # PUT /cameras/1.json
  def update
    @camera = Camera.find(params[:id])

		#checks if the cam can go to given direction
		unless @camera.can_go?params[:camera][:go_to_position]
			params[:camera][:go_to_position] = 'hold'
		end

    respond_to do |format|
      if @camera.update_attributes(params[:camera])
        format.html { redirect_to @camera, notice: 'Camera was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: "edit" }
        format.json { render json: @camera.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /cameras/1
  # DELETE /cameras/1.json
  def destroy
    @camera = Camera.find(params[:id])
    @camera.destroy

    respond_to do |format|
      format.html { redirect_to cameras_url }
      format.json { head :no_content }
    end
  end

  # GET /cameras/1/translade.json
  def translade
    @camera = Camera.find(params[:id])

    respond_to do |format|
	  	format.json { render :json => @camera, :only => [:id, :current_position, :go_to_position] }
    end  
  end

  # POST /camera/1/movements.json
  def movements
    @camera = Camera.find(params[:id])

	  #checks if the cam can go to given direction
	  unless @camera.can_go?((params[:camera])[:go_to_position])
		  params[:camera][:go_to_position] = 'hold'
	  end

    respond_to do |format|
      if @camera.update_attributes(params[:camera])
        format.json { head :no_content }
      else
        format.json { render json: @camera.errors, status: :unprocessable_entity }
      end
    end
  end

  #PUT /cameras/1/manual_control
  def manual_control
		@camera = Camera.find(params[:id])
		direction = params[:direction]

		#checks if the cam can go to given direction
	  if @camera.can_go? direction
      	@camera.go_to_position = direction
	  else
	    @camera.go_to_position = "hold"
	  end

    if @camera.save
  	  	redirect_to @camera
	  else
        flash[:error] = "#{@camera.errors}"
        redirect_to @camera
	  end
  end

	#POST /cameras/1/checkin.json
  def checkin
		@camera = Camera.find(params[:id])

    @camera.update_position
		@camera.save

		respond_to do |format|
      format.json { head :no_content }      
    end
  end

end
