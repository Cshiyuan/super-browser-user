"""
Google Gemini AI 客户端
"""

from typing import List, Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI

from ...utils.config import settings
from ...utils.logger import setup_logger


logger = setup_logger(__name__)


class GeminiClient:
    """Gemini AI 客户端封装"""

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        api_key: Optional[str] = None
    ):
        """
        初始化客户端

        Args:
            model: 模型名称（默认使用配置文件）
            temperature: 温度参数（默认使用配置文件）
            api_key: API 密钥（默认使用配置文件）
        """
        self.model = model or settings.GEMINI_MODEL
        self.temperature = temperature or settings.GEMINI_TEMPERATURE
        self.api_key = api_key or settings.GEMINI_API_KEY

        # 创建 LangChain 客户端
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model,
                temperature=self.temperature,
                google_api_key=self.api_key
            )
            logger.info(f"Gemini 客户端初始化完成: {self.model}")
        else:
            self.llm = None
            logger.warning("未提供 GEMINI_API_KEY，客户端将无法工作")

    async def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        发送聊天请求

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词

        Returns:
            AI 响应文本
        """
        try:
            # 构建消息
            messages = []
            if system_prompt:
                messages.append(("system", system_prompt))
            messages.append(("human", prompt))

            # 发送请求
            response = await self.llm.ainvoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Gemini API 调用失败: {e}")
            raise

    async def extract_structured_data(
        self,
        text: str,
        schema: Dict[str, Any],
        instruction: str = "请从以下文本中提取结构化数据"
    ) -> Dict[str, Any]:
        """
        提取结构化数据

        Args:
            text: 原始文本
            schema: 数据模式定义
            instruction: 提取指令

        Returns:
            提取的结构化数据
        """
        # 构建提示词
        schema_desc = self._format_schema(schema)
        prompt = f"""
{instruction}

数据格式要求:
{schema_desc}

原始文本:
{text}

请以 JSON 格式返回提取的数据。
"""

        try:
            response = await self.chat(prompt)

            # 解析 JSON 响应
            import json
            # 提取 JSON 部分（去除可能的 markdown 包装）
            json_text = response
            if "```json" in response:
                json_text = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_text = response.split("```")[1].split("```")[0].strip()

            return json.loads(json_text)

        except Exception as e:
            logger.error(f"结构化数据提取失败: {e}")
            raise

    async def extract_attractions(self, text: str) -> List[str]:
        """
        从文本中提取景点信息

        Args:
            text: 攻略文本

        Returns:
            景点列表
        """
        schema = {
            "attractions": ["string"]
        }

        result = await self.extract_structured_data(
            text=text,
            schema=schema,
            instruction="请从这篇旅游攻略中提取所有提到的景点名称"
        )

        return result.get("attractions", [])

    async def extract_restaurants(self, text: str) -> List[str]:
        """
        从文本中提取餐厅信息

        Args:
            text: 攻略文本

        Returns:
            餐厅列表
        """
        schema = {
            "restaurants": ["string"]
        }

        result = await self.extract_structured_data(
            text=text,
            schema=schema,
            instruction="请从这篇旅游攻略中提取所有提到的餐厅、美食店铺名称"
        )

        return result.get("restaurants", [])

    async def summarize_guides(
        self,
        guides: List[str],
        destination: str
    ) -> str:
        """
        总结多篇攻略

        Args:
            guides: 攻略文本列表
            destination: 目的地

        Returns:
            总结文本
        """
        combined_text = "\n\n---\n\n".join(guides)
        prompt = f"""
请总结以下关于 {destination} 的旅游攻略，提炼出关键信息：

{combined_text}

请包括：
1. 必游景点
2. 推荐美食
3. 交通建议
4. 住宿建议
5. 注意事项
"""

        return await self.chat(prompt)

    def _format_schema(self, schema: Dict[str, Any]) -> str:
        """格式化数据模式为文本描述"""
        import json
        return json.dumps(schema, indent=2, ensure_ascii=False)
