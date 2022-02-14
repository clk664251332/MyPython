--class("ConfirmScriptTools")
ConfirmScriptTools = {}
function ConfirmScriptTools:GetParam(key)
	return self.data[key]
end

function ConfirmScriptTools:HasId(id)
	return self.datas[id] ~= nil
end

function ConfirmScriptTools:GetConfig(id)
	if not self:HasId(id) then
		return false
	end

	self.data = self.datas[id]
	self.funcname = self.data.funcname
	return self
end


ConfirmScriptTools.datas = {
	[501401]=
	{
		funcname = "MonkSpiritSpheresCheck",
		["SpheresCountCost"] = 100,
	},
}

test = ConfirmScriptTools:GetConfig(501401)
if test then
	print(test:GetParam("SpheresCountCost"))
	print(test.funcname)
else
	print("找不到配置")
end