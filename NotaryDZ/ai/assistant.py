import os
import datetime
from dotenv import load_dotenv

load_dotenv()

class NotaryAIAssistant:
    def __init__(self):
        # We keep the structure for future API integration, but focus on the local engine
        pass

    def generate_contract(self, acte_type, client_data, bien_data):
        """
        Generates a professional contract draft using a local rule-based engine 
        tailored for Algerian law. No API key required.
        """
        # Clean input data
        info = client_data.get('info', '') + " " + bien_data.get('info', '')
        
        # Determine the template based on type
        if "VENTE" in acte_type:
            return self._generate_vente_template(info)
        elif "DON" in acte_type:
            return self._generate_don_template(info)
        elif "SOCIETE" in acte_type:
            return self._generate_societe_template(info)
        elif "PROCURATION" in acte_type:
            return self._generate_procuration_template(info)
        else:
            return self._generate_generic_template(acte_type, info)

    def _generate_vente_template(self, info):
        date_str = datetime.date.today().strftime("%Y/%m/%d")
        return f"""
الجمهورية الجزائرية الديمقراطية الشعبية
مكتب التوثيق: الأستاذ(ة) ....................
موثق بـ: ....................

عقد بيع عقاري (نموذج ذكي مدمج)
بتاريخ: {date_str}

أمامنا نحن الأستاذ(ة) .................... الموثق(ة) المذكور(ة) أعلاه، حضر الأطراف التالية أسماؤهم:

أولاً: البائع (أو البائعون)
الاسم واللقب: .................... المولود في: .................... بـ: ....................
المهنة: .................... الساكن بـ: ....................
الحالة المدنية: ....................

ثانياً: المشتري (أو المشترون)
الاسم واللقب: .................... المولود في: .................... بـ: ....................
المهنة: .................... الساكن بـ: ....................
الحالة المدنية: ....................

موضوع البيع:
بمقتضى هذا العقد، صرح البائع بأنه يبيع ويخصص تحت كافة الضمانات القانونية والفعلية للمشتري الذي يقبل منه العقار التالي بيانه:
{info if info else "[يرجى إدخال وصف العقار هنا]"}

أصل الملكية:
يصرح البائع أن العقار المبيع آل إليه بموجب .................... المسجل بـ .................... بتاريخ ....................

الثمن:
تم هذا البيع وقبل من الطرفين بمبلغ إجمالي قدره .................... دج.
صرح البائع بأنه قبض من يد المشتري المبلغ المذكور وأبرأ ذمته منه.

شروط عامة:
1. يحوز المشتري العقار المبيع ابتداءً من تاريخ التوقيع على هذا العقد.
2. يتحمل المشتري كافة الضرائب والرسوم المترتبة على هذا العقد.
3. يقر الطرفان بصحة البيانات الواردة أعلاه تحت طائلة بطلان العقد وفق القانون الجزائري.

تصريحات الأطراف (AML/KYC):
يصرح الأطراف أن هذه العملية المالية تتم وفقاً للقانون 05-01 المتعلق بالوقاية من غسل الأموال وتمويل الإرهاب.

توقيع الأطراف:                                  توقيع الموثق:
        """

    def _generate_procuration_template(self, info):
        return f"""
الجمهورية الجزائرية الديمقراطية الشعبية
مكتب التوثيق: ....................

وكالة عامة/خاصة
بتاريخ: {datetime.date.today().strftime("%Y/%m/%d")}

حضر أمامنا نحن الموثق المذكور أعلاه:
السيد(ة): .................... المولود(ة) في: .................... بـ: ....................
الساكن(ة) بـ: ....................

والذي صرح بمقتضى هذا العقد أنه يوكل عنه:
السيد(ة): .................... المولود(ة) في: .................... بـ: ....................
الساكن(ة) بـ: ....................

لينوب عنه في:
{info if info else "[يرجى تحديد غرض الوكالة هنا]"}

ولأجل ذلك، فإنه يمنح لوكيله كافة الصلاحيات اللازمة للقيام بالمهمة المذكورة أعلاه، بما في ذلك التوقيع على كافة الوثائق الإدارية والقانونية أمام الجهات المختصة.

توقيع الموكل:                                  توقيع الموثق:
        """

    def _generate_don_template(self, info):
        return f"عقد هبة (نموذج ذكي مدمج)\nبناءً على البيانات: {info}\n[يتم استكمال الصياغة القانونية للهبة وفق المذهب المالكي والقانون المدني الجزائري...]"

    def _generate_societe_template(self, info):
        return f"عقد تأسيس شركة (نموذج ذكي مدمج)\nبناءً على البيانات: {info}\n[يتم استكمال بنود القانون الأساسي للشركة وفق القانون التجاري الجزائري...]"

    def _generate_generic_template(self, type, info):
        return f"عقد {type}\nبناءً على البيانات: {info}\n[صياغة قانونية عامة...]"

    def compliance_check(self, client_name, amount):
        """
        Performs AML/KYC check locally.
        """
        risk_score = 0.0
        alerts = []
        
        # 50 million centimes = 500,000 DZD
        if amount >= 500000:
            risk_score += 0.6
            alerts.append("تنبيه قانوني (AML): المبلغ يتجاوز 50 مليون سنتيم. يجب التصريح لخلية معالجة الاستعلام المالي (CTRF) وفق القانون 05-01.")
        
        return {
            "risk_score": risk_score,
            "alerts": alerts,
            "status": "High Risk" if risk_score > 0.7 else "Medium Risk" if risk_score > 0.3 else "Low Risk"
        }
