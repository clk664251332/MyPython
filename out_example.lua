class("ConfirmScriptTools")

function ConfirmScriptTools:GetParam(key)
	return self.data[key]
end

function ConfirmScriptTools:HasId(id)
	return self.DATAS[id] ~= nil
end

function ConfirmScriptTools:GetConfig(id)
	if not self:HasId(id) then
		return false
	end

	self.data = self.DATAS[id]
	self.funcname = self.data.funcname
	return self
end

ConfirmScriptTools.DATAS = {
	[501401]=
	{
		funcname = "MonkSpiritSpheresCheck",
		["SpheresCountCost"] = 100,
	},
}

--[[test = ConfirmScriptTools:GetConfig(501401)
if test then
	print(test:GetParam("SpheresCountCost"))
	print(test.funcname)
else
	print("找不到配置")
end--]]