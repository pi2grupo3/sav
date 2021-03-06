require 'spec_helper'

describe WelcomeController do

  describe "GET 'sistemaintegrado'" do
    it "returns http success" do
      get 'sistemaintegrado'
      response.should be_success
    end
  end

  describe "GET 'index'" do
    it "returns http success" do
      get 'index'
      response.should be_success
    end
  end

  describe "GET 'seguranca'" do
    it "returns http success" do
      get 'seguranca'
      response.should be_success
    end
  end

  describe "GET 'poste'" do
    it "returns http success" do
      get 'poste'
      response.should be_success
    end
  end

  describe "GET 'monitoramento'" do
    it "returns http success" do
      get 'monitoramento'
      response.should be_success
    end
  end

  describe "GET 'contato'" do
    it "returns http success" do
      get 'contato'
      response.should be_success
    end
  end

end
