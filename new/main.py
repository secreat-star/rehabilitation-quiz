# -*- coding: utf-8 -*-
"""
康复医学答题软件 - Kivy Android版本
"""

import os
import json
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase

# ===================== 字体配置 =====================
# Android使用系统字体，确保中文显示
os.environ['KIVY_FONT'] = 'DroidSansFallback'
# ===================== 字体配置结束 =====================

class OptionButton(ButtonBehavior, BoxLayout):
    """选项按钮"""
    text = StringProperty('')
    letter = StringProperty('')
    is_correct = BooleanProperty(False)
    is_wrong = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        
        # 选项字母
        self.letter_label = Label(
            text=self.letter,
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#333333'),
            size_hint_x=0.1
        )
        
        # 选项文本
        self.text_label = Label(
            text=self.text,
            font_size=sp(16),
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_x=0.9,
            text_size=(Window.width * 0.7, None)
        )
        
        self.add_widget(self.letter_label)
        self.add_widget(self.text_label)
        
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.bind(is_correct=self._update_bg)
        self.bind(is_wrong=self._update_bg)
    
    def _update_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_correct:
                Color(*get_color_from_hex('#d4edda'))
            elif self.is_wrong:
                Color(*get_color_from_hex('#f8d7da'))
            else:
                Color(*get_color_from_hex('#ffffff'))
            
            RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[dp(5)]
            )

class MainMenu(BoxLayout):
    """主菜单界面"""
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(40), dp(20), dp(20)]
        self.spacing = dp(20)
        
        # 标题
        title = Label(
            text='康复医学\n答题练习软件',
            font_size=sp(32),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=0.3
        )
        self.add_widget(title)
        
        # 按钮容器
        btn_container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=0.6
        )
        
        # 菜单按钮
        buttons = [
            ('📚 练习模式', self.app.start_practice),
            ('📝 模拟考试', self.app.start_exam),
            ('🔁 错题重做', self.app.redo_wrong),
            ('🎲 随机练习', self.app.random_practice),
            ('📊 学习统计', self.app.show_stats),
            ('退出应用', self.app.stop_app)
        ]
        
        for btn_text, btn_callback in buttons:
            btn = Button(
                text=btn_text,
                font_size=sp(18),
                background_color=get_color_from_hex('#3498db'),
                color=get_color_from_hex('#ffffff'),
                size_hint_y=0.15
            )
            btn.bind(on_press=lambda instance, cb=btn_callback: cb())
            btn_container.add_widget(btn)
        
        self.add_widget(btn_container)

class QuestionScreen(BoxLayout):
    """答题界面"""
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        self.spacing = dp(10)
        
        # 顶部信息栏
        top_bar = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        
        self.back_btn = Button(
            text='◀ 返回',
            font_size=sp(14),
            size_hint_x=0.2,
            background_color=get_color_from_hex('#95a5a6')
        )
        self.back_btn.bind(on_press=self.app.go_back)
        
        self.info_label = Label(
            text='',
            font_size=sp(14),
            color=get_color_from_hex('#34495e'),
            halign='center'
        )
        
        self.score_label = Label(
            text='得分: 0/0',
            font_size=sp(14),
            color=get_color_from_hex('#27ae60'),
            size_hint_x=0.3
        )
        
        top_bar.add_widget(self.back_btn)
        top_bar.add_widget(self.info_label)
        top_bar.add_widget(self.score_label)
        self.add_widget(top_bar)
        
        # 题目区域（可滚动）
        question_scroll = ScrollView(size_hint_y=0.3)
        self.question_label = Label(
            text='',
            font_size=sp(18),
            color=get_color_from_hex('#2c3e50'),
            halign='left',
            valign='top',
            text_size=(Window.width - dp(30), None),
            size_hint_y=None
        )
        self.question_label.bind(texture_size=self.question_label.setter('height'))
        question_scroll.add_widget(self.question_label)
        self.add_widget(question_scroll)
        
        # 选项区域
        self.options_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=0.4
        )
        self.add_widget(self.options_layout)
        
        # 解析区域
        explanation_scroll = ScrollView(size_hint_y=0.22)
        self.explanation_label = Label(
            text='',
            font_size=sp(14),
            color=get_color_from_hex('#7f8c8d'),
            halign='left',
            valign='top',
            text_size=(Window.width - dp(30), None),
            size_hint_y=None
        )
        self.explanation_label.bind(texture_size=self.explanation_label.setter('height'))
        explanation_scroll.add_widget(self.explanation_label)
        self.add_widget(explanation_scroll)

class RehabQuizApp(App):
    """主应用类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "康复医学答题软件"
        self.questions = []
        self.current_questions = []
        self.current_index = 0
        self.score = 0
        self.total_answered = 0
        self.wrong_questions = []
        self.current_screen = None
        
        # 加载数据
        self.load_data()
    
    def build(self):
        # 设置窗口大小（适合手机）
        Window.size = (360, 640)
        Window.clearcolor = get_color_from_hex('#ecf0f1')
        
        # 创建主布局
        self.root_layout = BoxLayout()
        
        # 显示主菜单
        self.show_main_menu()
        
        return self.root_layout
    
    def load_data(self):
        """加载题目数据"""
        try:
            # 尝试从文件加载
            if os.path.exists('data/questions.json'):
                with open('data/questions.json', 'r', encoding='utf-8') as f:
                    self.questions = json.load(f)
            else:
                # 使用示例数据
                self.questions = [
                    {
                        "id": 1,
                        "question": "康复医学的主要对象是（ ）。",
                        "options": ["A. 残疾人", "B. 老年人", "C. 慢性病患者", "D. 以上都是"],
                        "answer": "D",
                        "explanation": "康复医学的对象包括残疾人、老年人、慢性病患者等。"
                    },
                    {
                        "id": 2,
                        "question": "测定F波的刺激量是（ ）。",
                        "options": [
                            "A. 超强刺激",
                            "B. 随意量刺激", 
                            "C. 刺激由小到大调整到恰大于M波阈强度",
                            "D. 阈下刺激"
                        ],
                        "answer": "A",
                        "explanation": "F波测定需要使用超强刺激才能获得稳定可靠的波形。"
                    },
                    {
                        "id": 3,
                        "question": "康复评定的目的是（ ）。",
                        "options": [
                            "A. 确定功能障碍的程度",
                            "B. 制定康复治疗方案",
                            "C. 评估康复治疗效果",
                            "D. 以上都是"
                        ],
                        "answer": "D",
                        "explanation": "康复评定的目的是确定功能障碍程度、制定治疗方案和评估治疗效果。"
                    }
                ]
        except Exception as e:
            print(f"加载数据错误: {e}")
            self.questions = []
    
    def show_main_menu(self):
        """显示主菜单"""
        self.root_layout.clear_widgets()
        self.current_screen = MainMenu(self)
        self.root_layout.add_widget(self.current_screen)
    
    def show_question_screen(self):
        """显示答题界面"""
        self.root_layout.clear_widgets()
        self.current_screen = QuestionScreen(self)
        self.root_layout.add_widget(self.current_screen)
        self.display_current_question()
    
    def display_current_question(self):
        """显示当前题目"""
        if not self.current_questions or self.current_index >= len(self.current_questions):
            self.show_results()
            return
        
        question = self.current_questions[self.current_index]
        
        # 更新题目信息
        self.current_screen.info_label.text = f"第 {self.current_index + 1}/{len(self.current_questions)} 题"
        self.current_screen.score_label.text = f"得分: {self.score}/{self.total_answered}"
        self.current_screen.question_label.text = question['question']
        self.current_screen.explanation_label.text = ""
        
        # 清空选项并添加新的
        self.current_screen.options_layout.clear_widgets()
        
        for option in question['options']:
            letter = option[0]  # 获取选项字母
            option_btn = OptionButton(
                text=option[2:],  # 去掉"A. "前缀
                letter=letter
            )
            option_btn.bind(on_press=lambda instance, l=letter: self.answer_question(l))
            self.current_screen.options_layout.add_widget(option_btn)
    
    def answer_question(self, answer):
        """回答问题"""
        question = self.current_questions[self.current_index]
        correct = (answer == question['answer'])
        
        # 更新分数
        self.total_answered += 1
        if correct:
            self.score += 1
        else:
            # 添加到错题集
            if question not in self.wrong_questions:
                self.wrong_questions.append(question)
        
        # 显示解析
        self.current_screen.explanation_label.text = f"{'✅ 回答正确！' if correct else '❌ 回答错误！'}\n\n解析：{question['explanation']}"
        
        # 高亮显示答案
        for child in self.current_screen.options_layout.children:
            if child.letter == question['answer']:
                child.is_correct = True
            elif child.letter == answer and not correct:
                child.is_wrong = True
        
        # 2秒后自动下一题
        Clock.schedule_once(lambda dt: self.next_question(), 2)
    
    def next_question(self):
        """下一题"""
        self.current_index += 1
        self.display_current_question()
    
    def start_practice(self, instance=None):
        """开始练习模式"""
        self.current_questions = self.questions.copy()
        self.current_index = 0
        self.score = 0
        self.total_answered = 0
        self.show_question_screen()
    
    def start_exam(self, instance=None):
        """开始模拟考试"""
        # 随机选择题目（最多20题）
        exam_questions = random.sample(self.questions, min(20, len(self.questions)))
        self.current_questions = exam_questions
        self.current_index = 0
        self.score = 0
        self.total_answered = 0
        self.show_question_screen()
        
        # 显示考试提示
        self.show_popup("模拟考试", "考试开始！\n\n共20题，请认真作答。")
    
    def redo_wrong(self, instance=None):
        """错题重做"""
        if not self.wrong_questions:
            self.show_popup("提示", "暂无错题记录")
            return
        
        self.current_questions = self.wrong_questions.copy()
        self.current_index = 0
        self.score = 0
        self.total_answered = 0
        self.show_question_screen()
    
    def random_practice(self, instance=None):
        """随机练习"""
        self.current_questions = random.sample(self.questions, len(self.questions))
        self.current_index = 0
        self.score = 0
        self.total_answered = 0
        self.show_question_screen()
    
    def show_stats(self, instance=None):
        """显示统计信息"""
        total = len(self.questions)
        accuracy = (self.score / self.total_answered * 100) if self.total_answered > 0 else 0
        
        stats_text = f"""
📊 学习统计：
────────────
总题数：{total}
已答题数：{self.total_answered}
答对题数：{self.score}
正确率：{accuracy:.1f}%
错题数：{len(self.wrong_questions)}
        """
        
        self.show_popup("学习统计", stats_text)
    
    def show_popup(self, title, message):
        """显示弹窗"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        label = Label(
            text=message,
            font_size=sp(16),
            halign='center',
            valign='middle'
        )
        content.add_widget(label)
        
        btn = Button(
            text="确定",
            size_hint_y=0.3,
            background_color=get_color_from_hex('#3498db')
        )
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()
    
    def show_results(self):
        """显示结果"""
        accuracy = (self.score / self.total_answered * 100) if self.total_answered > 0 else 0
        
        result_text = f"""
🎉 练习完成！
────────────
答题总数：{self.total_answered}
答对题数：{self.score}
正确率：{accuracy:.1f}%
        """
        
        if accuracy >= 80:
            result_text += "\n🎊 优秀！继续努力！"
        elif accuracy >= 60:
            result_text += "\n👍 良好，还有提升空间！"
        else:
            result_text += "\n💪 加油，多练习会更好！"
        
        self.show_popup("练习结果", result_text)
        self.show_main_menu()
    
    def go_back(self, instance=None):
        """返回上一界面"""
        self.show_main_menu()
    
    def stop_app(self, instance=None):
        """退出应用"""
        self.stop()

if __name__ == '__main__':
    RehabQuizApp().run()